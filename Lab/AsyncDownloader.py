import asyncio
import aiohttp
import os
from tqdm.notebook import tqdm
import nest_asyncio
from datetime import datetime
import os

# by inputing url + image file name pattern
class clsImageDownloader:
    # constructor
    def __init__(self):        
        self.image_urls = []
        self.image_folder = ""
        nest_asyncio.apply()
    # set parameters
    def setImageUrl(self, _url: str, _ext: str=".jpg", _min: int=1, _max: int=1):        
        self.image_urls = [ _url + self.threedigit(x) + _ext for x in range(_min, _max+1)]
        # for x in range(_min, _max+1):
        #     self.image_urls.append(_url + self.threedigit(x) + _ext)
    # set parameters
    def setImageFolder(self, _folder: str = ""):
        self.image_folder = _folder
    @staticmethod
    def threedigit(num: int) -> str:
        if num > 999:
            return num
        if num < 10:
            return f"00{str(num)}"
        if num < 100:
            return f"0{str(num)}"
        return str(num)
    @staticmethod
    def CreateFolderIfNotExist(_folder: str) -> bool:
        # Check whether the specified path exists or not
        isExist = os.path.exists(_folder)
        if isExist == True:
            return True
        else:
            # Create a new directory because it does not exist
            try:
                os.makedirs(_folder)
                print(f"The new directory {_folder} is created.")
                return True
            except:
                print(f"The directory {_folder} is NOT created!")
                return False
                
    @staticmethod
    def getNowTime():
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt
    
    async def download_image2(self, _url: str, _subfolder: str = ""):
        async with aiohttp.ClientSession() as session:
            async with session.get(_url) as response:
                fName = _url.split("/")[-1]
                if _subfolder == "":
                    fPath = 'C://Temp//all_images//'
                else:
                    fPath = f'C://Temp//all_images//{_subfolder}//'
                with open(fPath + fName, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                    print(fName, " is downloaded at: ", self.getNowTime(), ".")
                    
    def runIt(self) -> bool:
        isFolderExist_1 = self.CreateFolderIfNotExist('C://Temp')
        if isFolderExist_1 == False:
            return False
        isFolderExist_2 = self.CreateFolderIfNotExist('C://Temp//all_images')
        if isFolderExist_2 == False:
            return False
        isFolderExist_3 = self.CreateFolderIfNotExist('C://Temp//all_images//' + self.image_folder)
        if isFolderExist_3 == False:
            return False
        tasks = [self.download_image2(url, self.image_folder) for url in self.image_urls]
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        return True
      
# by input list of url(s) instead of url pattern
class clsSimpleDownloader:
    # constructor
    def __init__(self):        
        self.urls = []
        self.file_folder = ""
        nest_asyncio.apply()
    # set parameters
    def setImageUrl(self, _urls: list):        
        self.urls = _urls
    # set parameters
    def setImageFolder(self, _folder: str = ""):
        self.file_folder = _folder
    @staticmethod
    def CreateFolderIfNotExist(_folder: str) -> bool:
        # Check whether the specified path exists or not
        isExist = os.path.exists(_folder)
        if isExist == True:
            return True
        else:
            # Create a new directory because it does not exist
            try:
                os.makedirs(_folder)
                print(f"The new directory {_folder} is created.")
                return True
            except:
                print(f"The directory {_folder} is NOT created!")
                return False
                
    @staticmethod
    def getNowTime():
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt
    
    async def download_file2(self, _url: str, _subfolder: str = ""):
        async with aiohttp.ClientSession() as session:
            async with session.get(_url) as response:
                fName = _url.split("/")[-1]
                if _subfolder == "":
                    fPath = 'C://Temp//all_files//'
                else:
                    fPath = f'C://Temp//all_files//{_subfolder}//'
                with open(fPath + fName, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                    print(fName, " is downloaded at: ", self.getNowTime(), ".")
                    
    def runIt(self) -> bool:
        isFolderExist_1 = self.CreateFolderIfNotExist('C://Temp')
        if isFolderExist_1 == False:
            return False
        isFolderExist_2 = self.CreateFolderIfNotExist('C://Temp//all_files')
        if isFolderExist_2 == False:
            return False
        isFolderExist_3 = self.CreateFolderIfNotExist('C://Temp//all_files//' + self.file_folder)
        if isFolderExist_3 == False:
            return False
        tasks = [self.download_file2(url, self.file_folder) for url in self.urls]
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        return True