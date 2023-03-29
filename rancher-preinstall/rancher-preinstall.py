import wget
import json
import os
import ssl
import shutil

#This removes cert error
ssl._create_default_https_context = ssl._create_unverified_context


platform="windows"

#CPU can be modified depending on target CPU
cpu="amd64"

#THIS Must be updated for the target machine
root_dir = "/Users/raymonddolan"

#This is the config file to use.  Its located in the config dir
config_name =  "k3s-versions-limited.json"


#Do NOT CHANGE ANYTHING BELOW THIS
user_dir = os.path.join(root_dir,"Users","user_name")
cache_dir = os.path.join(user_dir,"AppData","Local","rancher-desktop","cache")
cache_out_dir = os.path.join(cache_dir,"k3s")
kubctl_out_dir = os.path.join(user_dir,".kuberlr")

k3s_url = "https://github.com/k3s-io/k3s/releases/download/{version}/"
k3s_files = ["k3s-airgap-images-amd64.tar","sha256sum-amd64.txt","k3s"]
kubectl = "https://dl.k8s.io/v{version}/bin/{platform}/{cpu}/kubectl.exe"


def build_target_dirs(k3_dir):
    try:
        os.makedirs(k3_dir)
    except:
        pass

def get_config_path(config_name):
    rel_path = "config" + os.sep + config_name
    full_path = os.path.abspath(rel_path)
    return full_path

def load_k3_config(config_name):
    full_path = get_config_path(config_name)
    f = open(full_path)
    data = json.load(f)
    f.close()
    return data["versions"]
  
def get_version_parts(version):
    p = version.split("+")
    return p[0][1:],p[1]

def main():
    versions = load_k3_config(config_name)

    #Build kubectl dir
    kubctl_dir = kubctl_out_dir + os.sep + platform + "-" + cpu
    build_target_dirs(kubctl_dir)

    #copy json file
    build_target_dirs(cache_dir)
    src_full_path = get_config_path(config_name)
    dest_path = cache_dir + os.sep + "k3s-versions.json"
    shutil.copy2(src_full_path, dest_path)

    #Download k3s versios
    for version in versions:
        ver_num,k3 = get_version_parts(version)

        #Download kubectl for k3s versions
        out_kubctl_file = kubctl_dir + os.sep + "kubectl" + ver_num + ".exe"
        url = kubectl.format(version=ver_num,platform=platform,cpu=cpu)        
        wget.download(url,out=out_kubctl_file)

        #Build k3s dir
        k3_dir = cache_out_dir + os.sep + version
        build_target_dirs(k3_dir)

        for file in k3s_files:
            
            url = k3s_url.format(version=version) + file
            out_k3_file = k3_dir + os.sep + file
            wget.download(url,out=out_k3_file)


        
    

if __name__  == "__main__":
    main()
    
    
