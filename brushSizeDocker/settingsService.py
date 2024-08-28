import os, json 

class SettingsService():
    
    def __init__(self) -> None:
        self.loadSettings()
        
    def loadSettings(self):
        json_setting = open(os.path.dirname(os.path.realpath(__file__)) + '/settings.json')
        self.setSettings(json.load(json_setting))
        json_setting.close()
        
    def setSettings(self, settings):
        self.settings = settings

    def getSettings(self):
        return self.settings

    def setDefaultMode(self, defaultMode: str):
        self.getSettings()["defaultMode"] = defaultMode

    def getDefaultMode(self) -> int:
        return int(self.settings["defaultMode"])

    def getModes(self) -> list[str]:
        modes =  [
            self.getSettings()["modes"]["small"]["label"],
            self.getSettings()["modes"]["medium"]["label"],
            self.getSettings()["modes"]["large"]["label"],
            self.getSettings()["modes"]["currentBrush"]["label"],
            self.getSettings()["modes"]["custom"]["label"]
        ]
        return modes
    
    def getDropdown(self) -> dict:
        modeMap = {
            self.getSettings()["modes"]["small"]["label"] : self.getSettings()["modes"]["small"]["key"],
            self.getSettings()["modes"]["medium"]["label"]: self.getSettings()["modes"]["medium"]["key"],
            self.getSettings()["modes"]["large"]["label"]: self.getSettings()["modes"]["large"]["key"],
            self.getSettings()["modes"]["currentBrush"]["label"]: self.getSettings()["modes"]["currentBrush"]["key"],
            self.getSettings()["modes"]["custom"]["label"]: self.getSettings()["modes"]["custom"]["key"]
        }
        return modeMap
    
    def getCustomSettings(self) -> dict:
        custom = self.getSettings()["modes"]["custom"]
        config = {
            "size1": {"size": custom["sizes"][0], "min": custom["ranges"][0]["min"], "max": custom["ranges"][0]["max"]},
            "size2": {"size": custom["sizes"][1], "min": custom["ranges"][1]["min"], "max": custom["ranges"][1]["max"]},
            "size3": {"size": custom["sizes"][2], "min": custom["ranges"][2]["min"], "max": custom["ranges"][2]["max"]},
            "size4": {"size": custom["sizes"][3], "min": custom["ranges"][3]["min"], "max": custom["ranges"][3]["max"]}
        }
        return config
    
    def getSmallSizes(self) -> list[int]:
        return self.getSizes("small")
    
    def getMediumSizes(self) -> list[int]:
        return self.getSizes("medium")
    
    def getLargeSizes(self) -> list[int]:
        return self.getSizes("large")
    
    def getCustomSizes(self) -> list[int]:
        return self.getSizes("custom")
    
    def getSizes(self, mode: str) -> list[int]:
        return list(self.getSettings()["modes"][mode]["sizes"])
    
    def getCustomRange(self, index: int):
        ranges = self.getSettings()["modes"]["custom"]["ranges"]
        return (ranges[index]["min"], ranges[index]["max"])
    
    def getIndexByMode(self, mode: str) -> int:
        return int(self.getSettings()["modes"][mode]["index"])
    
    def getDefaultModeString(self) -> str:
        return self.getSettings()["defaultMode"]
    
    def getDefaultModeInt(self) -> int:
        return self.getIndexByMode(self.getDefaultModeString())

    def setCustomSettings(self, customSettings: dict):
        
        sizes = [
            int(customSettings["size1"]["size"]),
            int(customSettings["size2"]["size"]),
            int(customSettings["size3"]["size"]),
            int(customSettings["size4"]["size"])
        ]

        ranges = [
            {"min": int(customSettings["size1"]["min"]), "max": int(customSettings["size1"]["max"])},
            {"min": int(customSettings["size2"]["min"]), "max": int(customSettings["size2"]["max"])},
            {"min": int(customSettings["size3"]["min"]), "max": int(customSettings["size3"]["max"])},
            {"min": int(customSettings["size4"]["min"]), "max": int(customSettings["size4"]["max"])}
        ]

        self.getSettings()["modes"]["custom"]["sizes"] = sizes
        self.getSettings()["modes"]["custom"]["ranges"] = ranges


    def saveSettings(self, defaultMode: str, customSettings: dict):
        self.setDefaultMode(defaultMode)
        self.setCustomSettings(customSettings)
        json_setting = json.dumps(self.getSettings(), indent = 4)
        with open(os.path.dirname(os.path.realpath(__file__)) + '/settings.json', "w") as outfile:
            outfile.write(json_setting)

    def toString(self):
        print(f"Brush size docker settings: {self.getSettings()}")