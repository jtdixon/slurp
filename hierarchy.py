import pandas as pd
import numpy as np
import requests, zipfile, io, re
from bs4 import BeautifulSoup

class Hierarchy(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.folders = []
        self.path_list = []
        self.current_paths = []
        self.paths = []
        self.files = []
        self.tags = []
        self.zips = []
        self.run()

    #Parse data and return all table elements
    def clean(self,filepath):
        r = requests.get(filepath, auth=('user', 'pass'))
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find('table')

        self.tags = data.find_all('a')
        return self.tags


    def find_folders(self):
        self.folders = [link.attrs['href'] for link in self.tags if (link.attrs['href'][-1:] == '/' and link.contents != ['Parent Directory'])]
        return self.folders

    def folder_update(self):
        for i in self.path_list:
            self.clean(i)
            self.find_folders()
            if len(self.folders) > 0:
                self.current_paths.append([i+x for x in self.folders])
            self.filepath = self.filepath.replace(i,'')
        self.paths.append([val for sublist in self.current_paths for val in sublist])

        #return self.path_list



    def find_files(self, path):
        #Get all zip files
        for link in self.tags:
            if link.attrs['href'][-3:] == 'zip':
                self.files.append(path+link.attrs['href'])

    def load_zip(self, f, path):
        # for f in self.files:
        r = requests.get(f)
        z = zipfile.ZipFile(io.BytesIO(r.content))

        z.extractall(path=path)



    def run(self):
        self.clean(self.filepath)
        self.find_folders()

        self.path_list = [quote_page+x for x in self.folders]
        self.paths.extend(([self.filepath], self.path_list))

        while len(self.path_list)>0:
            self.folder_update()
            #####flatten list
            self.path_list = [val for sublist in self.current_paths for val in sublist]
            self.folders = []
            self.current_paths = []

        self.paths = [path for subpath in [path for path in self.paths if path != []] for path in subpath]

        for path in self.paths:
            self.clean(path)
            self.find_files(path)

        #self.load_zip()



if __name__=='__main__':
    quote_page = 'https://www2.census.gov/acs/downloads/Core_Tables/rural_statistics_area/2007/Wyoming/'

    quote_list = Hierarchy(quote_page)

    for f in quote_list.files:
        file_name = quote_list.load_zip(f)
