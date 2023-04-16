class GlobalStatistic:
    def __init__(self, region_names, virus_names):
        self.region_names = region_names
        self.virus_names = virus_names
        state_dict = {"healthy": [], "sick": [], "immune": []}
        self.sick_data = {
            region_name: {virus_name: state_dict.copy() for virus_name in virus_names}
            for region_name in region_names + ["world"]
        }
        self.global_data = {
            region_name: {"healthy": [], "sick": []}
            for region_name in region_names + ["world"]
        }

    def add_data(self, step_num, region_name, region_statistic):
        h = region_statistic.get_healthy()
        s = region_statistic.get_sick()
        self.global_data[region_name]["healthy"].append(h)
        self.global_data[region_name]["sick"].append(s)

        for virus_name in self.virus_names:
            h = region_statistic.get_healthy(virus_name)
            s = region_statistic.get_sick(virus_name)
            i = region_statistic.get_immune(virus_name)
            self.sick_data[region_name][virus_name]["healthy"].append(h)
            self.sick_data[region_name][virus_name]["sick"].append(s)
            self.sick_data[region_name][virus_name]["immune"].append(i)

    def sum_step(self, step_num):
        h = s = 0
        for region_name in self.region_names:
            h += self.global_data[region_name]["healthy"][-1]
            s += self.global_data[region_name]["sick"][-1]
        self.global_data["world"]["healthy"].append(h)
        self.global_data["world"]["sick"].append(s)

        for virus_name in self.virus_names:
            h = s = i = 0
            for region_name in self.region_names:
                h += self.sick_data[region_name][virus_name]["healthy"][-1]
                s += self.sick_data[region_name][virus_name]["sick"][-1]
                i += self.sick_data[region_name][virus_name]["immune"][-1]
            self.sick_data["world"][virus_name]["healthy"].append(h)
            self.sick_data["world"][virus_name]["sick"].append(s)
            self.sick_data["world"][virus_name]["immune"].append(i)

    def get_global_window(self, size, region_name=None):
        if region_name is None:
            region_name = "world"
        h = self.global_data[region_name]["healthy"][-size:]
        s = self.global_data[region_name]["sick"][-size:]
        return h, s

    def get_sick_window(self, size, virus_name, region_name=None):
        if region_name is None:
            region_name = "world"
        h = self.sick_data[region_name][virus_name]["healthy"][-size:]
        s = self.sick_data[region_name][virus_name]["sick"][-size:]
        i = self.sick_data[region_name][virus_name]["immune"][-size:]
        return h, s, i
