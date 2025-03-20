#include "Map.h"

#include <cassert>
#include <cmath>
#include <iostream>
#include <filesystem>
#include <functional>
#include <queue>
#include <thread>
#include <string>
#include <utility>

#if defined(EVE_MAPPER_PYTHON) && EVE_MAPPER_PYTHON
#include <traceback_wrapper.h>
#else
#define Py_Trace_Errors(code) code void();
#endif

namespace bluemap {
    NullableColor::NullableColor() {
        is_null = true;
    }

    NullableColor::NullableColor(const uint_fast8_t red, const uint_fast8_t green, const uint_fast8_t blue): Color(
        red, green, blue) {
        is_null = false;
    }

    NullableColor::NullableColor(const uint_fast8_t red, const uint_fast8_t green, const uint_fast8_t blue,
                                 const uint_fast8_t alpha): Color(red, green, blue, alpha) {
        is_null = false;
    }

    NullableColor::NullableColor(const Color color): Color(color) {
        is_null = false;
    }

    Owner::Owner(const id_t id, std::string name, const int color_red, const int color_green, const int color_blue,
                 const bool is_npc): id(id),
                                     name(std::move(name)),
                                     color(color_red, color_green, color_blue),
                                     npc(is_npc) {
    }

    Owner::Owner(const id_t id, std::string name, const bool is_npc) : id(id),
                                                                       name(std::move(name)),
                                                                       color(NullableColor::null()),
                                                                       npc(is_npc) {
    }

    void Owner::increment_counter() {
        std::lock_guard lock(guard);
        count++;
    }

    id_t Owner::get_id() const {
        return id;
    }

    std::string Owner::get_name() const {
        return name;
    }

    void Owner::set_name(const std::string &name) {
        this->name = name;
    }

    NullableColor Owner::get_color() const {
        return color;
    }

    bool Owner::has_color() const {
        return !color.is_null;
    }

    void Owner::set_color(const NullableColor color) {
        this->color = color;
    }

    bool Owner::is_npc() const {
        return npc;
    }

    SolarSystem::SolarSystem(const id_t id, const id_t constellation_id, const id_t region_id, id_t x, id_t y): id(id),
        constellation_id(constellation_id),
        region_id(region_id), x(x), y(y) {
    }

    SolarSystem::SolarSystem(id_t id, id_t constellation_id, id_t region_id, unsigned int x, unsigned int y,
                             bool has_station, double sov_power, std::shared_ptr<Owner> owner)
        : id(id),
          constellation_id(constellation_id),
          region_id(region_id),
          x(x),
          y(y),
          has_station(has_station),
          sov_power(sov_power),
          owner(std::move(owner)) {
    }

    void SolarSystem::add_influence(const std::shared_ptr<Owner> &owner, double value) {
        assert(owner != nullptr);
        // Try and find the owner in the influences vector
        for (auto &influence: influences) {
            if (std::get<0>(influence) == owner) {
                // If the owner is found, update the influence value
                std::get<1>(influence) += value;
                return;
            }
        }
        // If the owner is not found, add a new influence
        influences.emplace_back(owner, value);
    }

    void SolarSystem::set_sov_power(double sov_power) {
        assert(sov_power >= 0.0);
        this->sov_power = sov_power;
    }

    id_t SolarSystem::get_id() const {
        return id;
    }

    id_t SolarSystem::get_constellation_id() const {
        return constellation_id;
    }

    id_t SolarSystem::get_region_id() const {
        return region_id;
    }

    bool SolarSystem::is_has_station() const {
        return has_station;
    }

    double SolarSystem::get_sov_power() const {
        return sov_power;
    }

    std::shared_ptr<Owner> SolarSystem::get_owner() const {
        return owner;
    }

    unsigned int SolarSystem::get_x() const {
        return x;
    }

    unsigned int SolarSystem::get_y() const {
        return y;
    }

    std::vector<std::tuple<std::shared_ptr<Owner>, double> > SolarSystem::get_influences() {
        return influences;
    }

    void Map::add_influence(const SolarSystem *solar_system, const std::shared_ptr<Owner> &owner, double value,
                            const double base_value, int distance) {
        assert(owner != nullptr);
        assert(solar_system != nullptr);
        std::vector<id_t> visited;
        std::vector<id_t> current;
        std::vector<id_t> next;

        current.push_back(solar_system->get_id());

        while (!current.empty()) {
            for (const auto s_id: current) {
                const auto sys = solar_systems[s_id];
                if (sys == nullptr) continue;
                if (std::find(visited.begin(), visited.end(), s_id) != visited.end()) continue;
                visited.push_back(s_id);
                sys->add_influence(owner, value);
                if (std::find(sov_solar_systems.begin(), sov_solar_systems.end(), sys.get()) == sov_solar_systems.
                    end()) {
                    sov_solar_systems.push_back(sys.get());
                }
                for (const auto &neighbor: connections[s_id]) {
                    if (std::find(visited.begin(), visited.end(), neighbor->get_id()) != visited.end()) continue;
                    next.push_back(neighbor->get_id());
                }
            }
            std::swap(current, next);
            next.clear();
            ++distance;
            if (power_max_distance >= 0 && distance >= power_max_distance) break;
            Py_Trace_Errors(value = power_falloff_function(value, base_value, distance);)
            if (value <= 0.0) break;
        }
    }

    Map::ColumnWorker::ColumnWorker(Map *map, const unsigned int start_x,
                                    const unsigned int end_x): map(map),
                                                               start_x(start_x),
                                                               end_x(end_x), cache(end_x - start_x, 16) {
        assert(map != nullptr);
        assert(start_x < end_x);
        this->render_old_owners = map->old_owners_image != nullptr;
    }

    std::tuple<Owner *, double> Map::ColumnWorker::calculate_influence(unsigned int x, unsigned int y) const {
        std::map<Owner *, double> total_influence = {};
        for (auto &solar_system: map->sov_solar_systems) {
            assert(solar_system != nullptr);
            const int dx = static_cast<int>(x) - static_cast<int>(solar_system->get_x());
            const int dy = static_cast<int>(y) - static_cast<int>(solar_system->get_y());
            const double dist_sq = dx * dx + dy * dy;
            if (dist_sq > 160000) continue;
            for (auto &[owner, power]: solar_system->get_influences()) {
                assert(owner != nullptr);
                //const auto res = total_influence.try_emplace(owner, 0.0);
                const double old = total_influence[owner.get()];
                total_influence[owner.get()] = old + power / (500 + dist_sq);
            }
        }
        double best_influence = 0.0;
        Owner *best_owner = nullptr;
        for (const auto &[owner, influence]: total_influence) {
            if (influence > best_influence) {
                best_owner = owner;
                best_influence = influence;
            }
        }
        if (best_influence < 0.023) best_owner = nullptr;
        return {best_owner, best_influence};
    }

    void Map::ColumnWorker::process_pixel(
        const unsigned int width,
        const unsigned int i,
        const unsigned int y,
        std::vector<Owner *> &this_row,
        const std::vector<Owner *> &prev_row,
        std::vector<double> &prev_influence,
        std::vector<bool> &border
    ) const {
        const unsigned int x = start_x + i;
        auto [owner, influence] = calculate_influence(x, y);

        this_row[i] = owner;

        // Draw image
        const bool owner_changed = prev_row[i] == nullptr && owner != nullptr ||
                                   prev_row[i] != nullptr && owner == nullptr ||
                                   prev_row[i] != nullptr && prev_row[i] != owner;
        if (y > 0) {
            if (
                const auto prev_owner = prev_row[i];
                prev_owner != nullptr && !prev_owner->is_npc()
            ) {
                const bool draw_border = border[i] || owner_changed ||
                                         i > 0 && prev_row[i - 1] != prev_row[i] ||
                                         i < width - 1 && prev_row[i + 1] != prev_row[i];
                int alpha;
                Py_Trace_Errors(alpha = static_cast<int>(map->influence_to_alpha(prev_influence[i]));)
                if (!prev_owner->is_npc()) {
                    if (!prev_owner->has_color()) {
                        Color new_color;
                        Py_Trace_Errors(new_color = map->generate_owner_color(prev_owner->get_id());)
                        prev_owner->set_color(new_color);
                    }
                    const auto color = prev_owner->get_color().with_alpha(
                        draw_border ? std::max(map->border_alpha, alpha) : alpha
                    );
                    cache.set_pixel(i, y - row_offset, color);
                } else {
                    cache.set_pixel(i, y - row_offset, {0, 0, 0, 0});
                }

                if (render_old_owners) {
                    if (const auto old_owner_id = map->old_owners_image.get()[x + y * map->get_width()];
                        old_owner_id != 0 && old_owner_id != prev_owner->get_id()
                    ) {
                        const auto old_owner = map->owners[old_owner_id];
                        if (old_owner != nullptr && !old_owner->is_npc()) {
                            Color old_color = {255, 255, 255};
                            if (!old_owner->has_color()) {
                                Color new_color;
                                Py_Trace_Errors(new_color = map->generate_owner_color(old_owner->get_id());)
                                old_owner->set_color(new_color);
                            }
                            old_color = static_cast<Color>(old_owner->get_color()); // NOLINT(*-slicing)

                            if (constexpr int slant = 5;
                                (y % slant + x) % slant == 0
                            ) {
                                cache.set_pixel(i, y - row_offset, old_color.with_alpha(alpha));
                            }
                        }
                    }
                }
            }
        }
        if (owner != nullptr) {
            owner->increment_counter();
            const size_t index = x + y * map->width;
            map->owner_image.get()[index] = owner;
        }

        prev_influence[i] = influence;
        border[i] = y == 0 || owner_changed;
    }

    void Map::ColumnWorker::render() {
        std::lock_guard render_lock(render_mutex);
        std::shared_lock map_lock(map->map_mutex);

        const unsigned int width = end_x - start_x;
        const unsigned int height = map->get_height();
        std::vector<Owner *> this_row(width);
        std::vector<Owner *> prev_row(width);
        std::vector<bool> border(width);
        std::vector<double> prev_influence(width);

        for (unsigned int y = 0; y < height; ++y) {
            for (unsigned int i = 0; i < width; ++i) {
                Py_Trace_Errors(process_pixel(width, i, y, this_row, prev_row, prev_influence, border);)
            }

            const auto t = prev_row;
            prev_row = this_row;
            this_row = t;
            if (y > row_offset && y - row_offset == 15) {
                map->paste_cache(start_x, y - 15, cache);
                row_offset = y + 1;
                cache.reset();
                // Fuck C why the hell did this line cause so much trouble: cache = Image(width, 16);
            }
        }
        // Paste the remaining cache
        map->paste_cache(start_x, row_offset, cache, height - row_offset);
    }

    Map::MapOwnerLabel::MapOwnerLabel() = default;

    Map::MapOwnerLabel::MapOwnerLabel(const id_t owner_id): owner_id(owner_id) {
    }

    /**
     *
     * Performs a flood fill on the owner_image to detect connected regions of the same owner
     * As a result, all entries in the owner_image will be set to nullptr
     *
     * @param x the x coordinate to start the flood fill
     * @param y the y coordinate
     * @param label the label to detect the region
     */
    void Map::owner_flood_fill(unsigned int x, unsigned int y, MapOwnerLabel &label) {
        std::queue<std::pair<unsigned int, unsigned int> > q;
        q.emplace(x, y);

        while (!q.empty()) {
            auto [cx, cy] = q.front();
            q.pop();

            const size_t index = cx + cy * width;
            if (owner_image[index] == nullptr || owner_image[index]->get_id() != label.owner_id) {
                continue;
            }

            // Set the current pixel to nullptr
            owner_image[index] = nullptr;
            ++label.count;
            label.x += cx;
            label.y += cy;

            // Add neighboring pixels to the queue
            if (cx >= sample_rate) q.emplace(cx - sample_rate, cy);
            if (cx + sample_rate < width) q.emplace(cx + sample_rate, cy);
            if (cy >= sample_rate) q.emplace(cx, cy - sample_rate);
            if (cy + sample_rate < height) q.emplace(cx, cy + sample_rate);
        }
    }

    Map::Map() {
        this->owner_image = std::make_unique<Owner *[]>(width * height);

        sov_power_function = [](const double sov_power, bool, id_t) {
            double influence = 10.0;
            if (sov_power >= 6.0) {
                influence *= 6;
            } else {
                influence *= sov_power / 2.0;
            }
            return influence;
        };

        power_falloff_function = [](const double value, double, int) {
            return value * 0.3;
        };

        influence_to_alpha = [](const double influence) {
            return std::min(
                190,
                static_cast<int>(std::log(std::log(influence + 1.0) + 1.0) * 700));
        };

        generate_owner_color = [](const id_t owner_id) {
            const int r = static_cast<int>(owner_id * 811) % 256;
            const int g = static_cast<int>(owner_id * 1321) % 256;
            const int b = static_cast<int>(owner_id * 1931) % 256;
            return NullableColor(r, g, b);
        };
    }

    Map::~Map() = default;

    void Map::clear() {
        std::unique_lock lock(map_mutex);
        owners.clear();
        solar_systems.clear();
        connections.clear();
        sov_solar_systems.clear();
        owner_image = nullptr;
    }

    void Map::update_size(const unsigned int width, const unsigned int height, const unsigned int sample_rate) {
        std::unique_lock lock(map_mutex);
        this->width = width;
        this->height = height;
        this->sample_rate = sample_rate;
        image.resize(width, height);
        owner_image = std::make_unique<Owner *[]>(width * height);
        old_owners_image = nullptr;
    }

    void Map::load_data(const std::string &filename) {
        std::unique_lock lock(map_mutex);
        std::ifstream file(filename, std::ios::binary);
        if (!file) {
            throw std::runtime_error("Unable to open file");
        }

        int owner_size = read_big_endian<int32_t>(file);
        LOG("Loading " << owner_size << " owners")
        for (int i = 0; i < owner_size; ++i) {
            int id = read_big_endian<int32_t>(file);
            int name_length = read_big_endian<uint16_t>(file);
            std::string name(name_length, '\0');
            file.read(&name[0], name_length);
            int color_red = read_big_endian<int32_t>(file);
            int color_green = read_big_endian<int32_t>(file);
            int color_blue = read_big_endian<int32_t>(file);
            int is_npc = read_big_endian<uint8_t>(file);
            std::shared_ptr<Owner> owner = std::make_shared<Owner>(
                id, name, color_red, color_green, color_blue, is_npc);
            owners[id] = owner;
        }

        int systems_size = read_big_endian<int32_t>(file);
        LOG("Loading " << systems_size << " solar systems")
        for (int i = 0; i < systems_size; ++i) {
            int id = read_big_endian<int32_t>(file);
            int x = read_big_endian<int32_t>(file);
            int y = read_big_endian<int32_t>(file);
            int region_id = read_big_endian<int32_t>(file);
            int constellation_id = read_big_endian<int32_t>(file);
            int has_station = read_big_endian<uint8_t>(file);
            auto adm = read_big_endian<double>(file);
            int sovereignty_id = read_big_endian<int32_t>(file);

            std::shared_ptr<Owner> sovereignty = (sovereignty_id == 0) ? nullptr : owners[sovereignty_id];
            solar_systems[id] = std::make_shared<SolarSystem>(id, constellation_id, region_id, x, y, has_station, adm,
                                                              sovereignty);
        }

        int jumps_table_size = read_big_endian<int32_t>(file);
        LOG("Loading " << jumps_table_size << " connections")
        for (int i = 0; i < jumps_table_size; ++i) {
            int key_id = read_big_endian<int32_t>(file);
            int value_size = read_big_endian<int32_t>(file);

            std::vector<SolarSystem *> value;
            value.reserve(value_size);
            for (int j = 0; j < value_size; ++j) {
                int ss_id = read_big_endian<int32_t>(file);
                value.push_back(solar_systems[ss_id].get());
            }
            connections[key_id] = value;
        }
        LOG("Loaded " << owners.size() << " owners, " << solar_systems.size() << " solar systems, and "
            << connections.size() << " connections")
    }

    void Map::load_data(const std::vector<OwnerData> &owners, const std::vector<SolarSystemData> &solar_systems,
                        const std::vector<JumpData> &jumps) {
        std::unique_lock lock(map_mutex);
        for (const auto &owner_data: owners) {
            if (owner_data.color)
                this->owners[owner_data.id] = std::make_shared<Owner>(
                    owner_data.id, "", owner_data.color.red,
                    owner_data.color.green, owner_data.color.blue, owner_data.npc
                );
            else
                this->owners[owner_data.id] = std::make_shared<Owner>(
                    owner_data.id, "", owner_data.npc
                );
        }
        for (const auto &solar_system_data: solar_systems) {
            this->solar_systems[solar_system_data.id] = std::make_shared<SolarSystem>(
                solar_system_data.id,
                solar_system_data.constellation_id,
                solar_system_data.region_id,
                solar_system_data.x,
                solar_system_data.y,
                solar_system_data.has_station,
                solar_system_data.sov_power,
                solar_system_data.owner == 0
                    ? nullptr
                    : this->owners[solar_system_data.owner]
            );
        }
        for (const auto &[sys_from, sys_to]: jumps) {
            connections[sys_from].push_back(this->solar_systems[sys_to].get());
        }
    }

    void Map::set_data(const std::vector<std::shared_ptr<Owner> > &owners,
                       const std::vector<std::shared_ptr<SolarSystem> > &solar_systems,
                       const std::vector<JumpData> &jumps) {
        std::unique_lock lock(map_mutex);
        for (const auto &owner: owners) {
            this->owners[owner->get_id()] = owner;
        }
        for (const auto &solar_system: solar_systems) {
            this->solar_systems[solar_system->get_id()] = solar_system;
        }
        for (const auto &[sys_from, sys_to]: jumps) {
            connections[sys_from].push_back(this->solar_systems[sys_to].get());
        }
    }

    void Map::set_sov_power_function(std::function<double(double, bool, id_t)> sov_power_function) {
        std::unique_lock lock(map_mutex);
        this->sov_power_function = std::move(sov_power_function);
    }

    void Map::set_power_falloff_function(std::function<double(double, double, int)> power_falloff_function) {
        std::unique_lock lock(map_mutex);
        this->power_falloff_function = std::move(power_falloff_function);
    }

    void Map::set_influence_to_alpha_function(std::function<double(double)> influence_to_alpha) {
        std::unique_lock lock(map_mutex);
        this->influence_to_alpha = std::move(influence_to_alpha);
    }

    void Map::calculate_influence() {
        std::unique_lock lock(map_mutex);
        if (sov_solar_systems.empty()) {
            for (const auto &sys: solar_systems) {
                if (sys.second->get_owner() != nullptr) {
                    sov_solar_systems.push_back(sys.second.get());
                }
            }
        }
        LOG("Calculating influence for " << sov_solar_systems.size() << " solar systems")
        auto sov_orig = sov_solar_systems;

        for (const auto &solar_system: sov_orig) {
            const id_t owner_id = solar_system->get_owner() == nullptr ? 0 : solar_system->get_owner()->get_id();
            double influence;
            Py_Trace_Errors(
                influence = sov_power_function(
                    solar_system->get_sov_power(),
                    solar_system->is_has_station(),
                    owner_id);)
            const int level = (solar_system->get_sov_power() >= 6.0) ? 1 : 2;
            Py_Trace_Errors(
                add_influence(solar_system, solar_system->get_owner(), influence, influence, level);)
        }
    }

    void Map::render_multithreaded() {
        const unsigned int thread_count = std::thread::hardware_concurrency();
        std::vector<std::thread> threads;
        std::vector<ColumnWorker *> workers;
        LOG("Starting " << thread_count << " threads")
        for (int i = 0; i < thread_count; ++i) {
            const unsigned int start_x = i * width / thread_count;
            const unsigned int end_x = (i + 1) * width / thread_count;
            workers.emplace_back(create_worker(start_x, end_x));
            //std::cout << "Starting thread " << i << " with x range " << start_x << " to " << end_x << std::endl;
            threads.emplace_back(&ColumnWorker::render, workers.back());
        }
        LOG("Waiting for threads to finish")
        for (auto &thread: threads) {
            if (thread.joinable())
                thread.join();
        }
        for (const auto worker: workers) {
            delete worker;
        }
        LOG("Rendering completed")
    }

    std::vector<Map::MapOwnerLabel> Map::calculate_labels() {
        std::unique_lock lock(map_mutex);
        std::vector<MapOwnerLabel> labels;
        // Iterate over all pixels according to the sample rate
        for (unsigned int y = 0; y < height; y += sample_rate) {
            for (unsigned int x = 0; x < width; x += sample_rate) {
                // Get the owner at the current pixel
                const Owner *owner = owner_image.get()[x + y * width];
                if (owner == nullptr) {
                    continue;
                }
                if (owner->is_npc()) {
                    continue;
                }
                auto label = MapOwnerLabel{owner->get_id()};
                owner_flood_fill(x, y, label);
                label.x = label.x / label.count + sample_rate / 2;
                label.y = label.y / label.count + sample_rate / 2;
                labels.push_back(label);
            }
        }
        return labels;
    }

    Map::ColumnWorker *Map::create_worker(unsigned int start_x, unsigned int end_x) {
        image.alloc();
        return new ColumnWorker(this, start_x, end_x);
    }

    void Map::paste_cache(const unsigned int start_x, const unsigned int start_y, const Image &cache, int height) {
        std::lock_guard lock(image_mutex);
        if (height == -1) {
            height = cache.get_height();
        }
        for (unsigned int y = 0; y < height; ++y) {
            for (unsigned int x = 0; x < cache.get_width(); ++x) {
                auto [r, g, b, a] = cache.get_pixel(x, y);
                image.set_pixel(start_x + x, start_y + y, r, g, b, a);
            }
        }
    }

    void Map::save_owner_image(const std::string &filename) const {
        std::ofstream file(filename, std::ios::binary);
        if (!file) {
            throw std::runtime_error("Unable to open file");
        }
        file.write("SOVNV1.0", 8);
        // Write header with width and height
        write_big_endian<int32_t>(file, width);
        write_big_endian<int32_t>(file, height);
        // Write the owner ids
        for (unsigned int x = 0; x < width; ++x) {
            for (unsigned int y = 0; y < height; ++y) {
                if (const Owner *owner = owner_image.get()[x + y * width]; owner == nullptr) {
                    write_big_endian<int64_t>(file, -1);
                } else {
                    write_big_endian<int64_t>(file, static_cast<int64_t>(owner->get_id()));
                }
            }
        }
        file.close();
    }

    void Map::load_old_owners(const std::string &filename) {
        std::unique_lock lock(map_mutex);
        std::ifstream file(filename, std::ios::binary);
        if (!file) {
            throw std::runtime_error("Unable to open file");
        }
        // Read the header
        char header[8] = {0};
        file.read(header, 8);
        if (std::string(header, 8) != "SOVNV1.0") {
            throw std::runtime_error("Invalid file format: " + std::string(header, 8));
        }
        // Read the width and height
        const auto file_width = read_big_endian<int32_t>(file);
        const auto file_height = read_big_endian<int32_t>(file);
        if (file_width != width || file_height != height) {
            throw std::runtime_error("Invalid file dimensions, expected " + std::to_string(width) + "x" +
                                     std::to_string(height) + " but got " + std::to_string(file_width) + "x" +
                                     std::to_string(file_height));
        }
        old_owners_image = std::make_unique<id_t[]>(width * height);
        // Read the owner ids
        for (unsigned int x = 0; x < width; ++x) {
            for (unsigned int y = 0; y < height; ++y) {
                const auto owner_id = read_big_endian<int64_t>(file);
                if (x == 1335 && y == 25) {
                    LOG(owner_id << " into " << (x + y * width))
                }
                if (owner_id == -1) {
                    old_owners_image.get()[x + y * width] = 0;
                } else {
                    old_owners_image.get()[x + y * width] = owner_id;
                }
            }
        }
        file.close();
    }

    void Map::debug_save_old_owners(const std::string &filename) const {
        Image debug_image(width, height);
        for (unsigned int x = 0; x < width; ++x) {
            for (unsigned int y = 0; y < height; ++y) {
                const auto owner_id = old_owners_image.get()[x + y * width];
                if (owner_id == 0) {
                    debug_image.set_pixel(x, y, 0, 0, 0);
                } else {
                    const auto owner = owners.at(owner_id);
                    debug_image.set_pixel(x, y, owner->get_color().with_alpha(255));
                }
            }
        }
        debug_image.write(filename.c_str());
    }

    void Map::save(const std::string &filename) const {
        std::unique_lock lock(map_mutex);
        image.write(filename.c_str());
    }

    uint8_t *Map::retrieve_image() {
        std::unique_lock lock(map_mutex);
        return image.retrieve_data();
    }

    id_t *Map::create_owner_image() const {
        const auto owner_image = new id_t[width * height];
        for (unsigned int x = 0; x < width; ++x) {
            for (unsigned int y = 0; y < height; ++y) {
                const auto owner = this->owner_image.get()[x + y * width];
                if (owner == nullptr) {
                    owner_image[x + y * width] = 0;
                } else {
                    owner_image[x + y * width] = owner->get_id();
                }
            }
        }
        return owner_image;
    }

    void Map::set_old_owner_image(id_t *old_owner_image, const unsigned int width, const unsigned int height) {
        std::unique_lock lock(map_mutex);
        this->old_owners_image = std::unique_ptr<id_t[]>(old_owner_image);
        if (this->width != width || this->height != height) {
            this->old_owners_image = nullptr;
            throw std::runtime_error(
                "Invalid dimensions for old owner image, expected " +
                std::to_string(this->width) + "x" + std::to_string(this->height) + " but got " +
                std::to_string(width) + "x" + std::to_string(height));
        }
    }

    unsigned int Map::get_width() const {
        return width;
    }

    unsigned int Map::get_height() const {
        return height;
    }

    bool Map::has_old_owner_image() const {
        return old_owners_image != nullptr;
    }
#if defined(EVE_MAPPER_PYTHON) && EVE_MAPPER_PYTHON
    void Map::set_sov_power_function(PyObject *pyfunc) {
        std::unique_lock lock(map_mutex);
        sov_power_pyfunc = std::make_unique<py::Callable<double, double, bool, id_t> >(pyfunc);
        if (!sov_power_pyfunc->validate()) {
            sov_power_pyfunc = nullptr;
            throw std::runtime_error(
                "Invalid callable, expected a function with signature (double, bool, int) -> double");
        }
        sov_power_function = [this](const double sov_power, const bool has_station, const id_t owner_id) {
            Py_Trace_Errors(
                return (*sov_power_pyfunc)(sov_power, has_station, owner_id);)
        };
    }

    void Map::set_power_falloff_function(PyObject *pyfunc) {
        std::unique_lock lock(map_mutex);
        power_falloff_pyfunc = std::make_unique<py::Callable<double, double, double, int> >(pyfunc);
        if (!power_falloff_pyfunc->validate()) {
            power_falloff_pyfunc = nullptr;
            throw std::runtime_error(
                "Invalid callable, expected a function with signature (double, double, int) -> double");
        }
        power_falloff_function = [this](const double value, const double base_value, const int distance) {
            Py_Trace_Errors(
                return (*power_falloff_pyfunc)(value, base_value, distance);)
        };
    }

    void Map::set_influence_to_alpha_function(PyObject *pyfunc) {
        std::unique_lock lock(map_mutex);
        influence_to_alpha_pyfunc = std::make_unique<py::Callable<double, double> >(pyfunc);
        if (!influence_to_alpha_pyfunc->validate()) {
            influence_to_alpha_pyfunc = nullptr;
            throw std::runtime_error("Invalid callable, expected a function with signature (double) -> double");
        }
        influence_to_alpha = [this](const double influence) {
            Py_Trace_Errors(
                return (*influence_to_alpha_pyfunc)(influence);)
        };
    }

    void Map::set_generate_owner_color_function(PyObject *pyfunc) {
        std::unique_lock lock(map_mutex);
        generate_owner_color_pyfunc = std::make_unique<py::Callable<std::tuple<int, int, int>, id_t> >(pyfunc);
        if (!generate_owner_color_pyfunc->validate()) {
            generate_owner_color_pyfunc = nullptr;
            throw std::runtime_error(
                "Invalid callable, expected a function with signature (int) -> tuple[int, int, int]");
        }
        generate_owner_color = [this](const id_t owner_id) {
            std::tuple<int, int, int> color;
            Py_Trace_Errors(
                color = (*generate_owner_color_pyfunc)(owner_id);)
            return Color(color);
        };
    }
#endif
} // EveMap
