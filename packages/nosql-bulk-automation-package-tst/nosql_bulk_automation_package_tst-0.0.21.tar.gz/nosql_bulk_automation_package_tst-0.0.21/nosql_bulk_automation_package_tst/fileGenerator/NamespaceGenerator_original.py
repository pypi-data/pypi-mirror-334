import os
import yaml

from nosql_bulk_automation_package_tst.fileGenerator.ArgocdPhase import ArgocdPhase
import nosql_bulk_automation_package_tst.refernce_file_constants as refs


class NamespaceGenerator:
    def __init__(self):
        print('\n'+40*'#',end='\n\n')
        print('NamespaceGenerator')
        print('\n'+40*'#',end='\n\n')
    
    def datastore_nano_id(self,datastore):
        if datastore == 'couchbase':
            return '24e948d1-5bc6-11e7-a4b8-0050560c4716'
        elif datastore == 'mongodb':
            return '24e948d9-5bc6-11e7-a4b8-0050560c4716'
        elif datastore == 'Elasticsearch':
            return '24e996f8-5bc6-11e7-a4b8-0050560c4716'
        else:
            print("error : no matching datasore nano in namespace")
            exit(0)
        
    def namespaceGenerator(self,datastore,app,paas_name,phase,types):

        dc_prov="az"
        secZone="tnz"

        ns_file={}
        truePhase=ArgocdPhase.get_phase(phase,paas_name.split('-'))
        # ns_phase='prd' if phase in ['prd','ppt','ccp'] else 'tst'
        ns_phase=truePhase
 
        ns_version=''
        ref_file_path = refs.namespace_ref_file_path.replace("@type@", types)
        
        # ref_file= open(f"../reference/{(datastore.lower())}-exporter/@namespace@-@region@-@phase@-@exporterId@.yaml",'r')
        ref_file= open(ref_file_path,'r')
        # ref_file=yaml.safe_load(ref_file)
        ref_file=ref_file.readlines()
        # print(ref_file)
        for i in ref_file:
            if 'deployerChartVersion' in i and 'deployerChartVersion: "1.0"' not in i:
                ns_version=i
                print(i)
                # exit(1)
        # print((ref_file[f'{(datastore.lower())}Exporter']["namespace"]))
        # exit(0)
        ns_version=(ns_version.replace("deployerChartVersion: ","")).strip()
        ns_version=(ns_version.strip("''""\""))

        if datastore=='Elasticsearch':
            ns_type='Elasticsearch'
            ns='elk'
        elif datastore=="Couchbase":
            ns_type='couchbase'
            ns='couchbase'
        else:
            ns_type='mongodb'
            ns='mongodb'
        ns_file['name']=f'datastore-{ns}-{types}-{app}'
        if paas_name in ["nld10","nld7","nld8","nld9","prd-we-tcp01","prd-we-tcp02","tst-we-cytr01","eus1","eus2","eus3","eus4"]:
            ns_file['calico']=True
        else:
            ns_file['calico']=False
        if ns_file['calico']:
            ns_file['JenkinsNamespace']='datastore-tools'
        ns_file['dcProv']=dc_prov
        ns_file['quota']=f'dbaas-{datastore.lower()}'
        ns_file['quotaAdminGroup']=f'amacp-{ns_phase}-dbaas-nosql-paas-admins'
        ns_file['deployerChartVersion']=ns_version
        ns_file['labels']={}
        ns_file['roles']={}
        ns_file['shouldInstallkv2role']={}
        ns_file['labels']['acs.amadeus.com/environment']=ns_phase
        ns_file['labels']['acs.amadeus.com/securityZone']=secZone
        ns_file['labels']['app.kubernetes.io/part-of']=ns_type
        ns_file['labels']['paas.amadeus.net/quota']=f'dbaas-{datastore.lower()}'
        ns_file['annotations']={}
        ns_file['annotations']['acs.amadeus.com/service-id']=self.datastore_nano_id(ns_type)
        ns_file['namespaceRoleTypes']={}
        ns_file['namespaceRoleTypes']=["app"]
        ns_file['paas']=paas_name
        ns_file['roles']['admin']={}
        ns_file['roles']['admin']['groups']=[]
        ns_file['roles']['admin']['groups'].append("dbaas.nosql.devops")
        if dc_prov=='az':
            ns_file['roles']['admin']['groups'].append(f"amacp-{ns_phase}-dbaas-nosql-paas-admins")
            # ns_file['roles']['admin']['groups'].append(f"amacp-{ns_phase}-dbaas-nosql-{ns_type.lower()}-contributors")
            ns_file['shouldInstallkv2role']["enabled"]=True
            
        if phase=="rnd":
            ns_file['roles']['admin']['groups'].append("GTC-PSV-DSS-NSQ-NSK")

        ns_file["token_name"]="quota-admin"
        ns_file["argocdSuffix"]=False
        ns_file['setup-namespace-job']={}
        ns_file["setup-namespace-job"]["version"]="1.0"
        
        print( yaml.dump(ns_file))       
        path=f'dummyInventory/argocd-nosqlpaas-{truePhase}/{truePhase}/az/{paas_name}'
        if not os.path.exists(f"{path}/namespace"):
            os.makedirs(f"{path}/namespace")
            print("The new namespace directory is created!")
        with open(f'{path}/namespace/datastore-{ns}-{types}-{app}.yaml', 'w+',) as f :
            yaml.dump(ns_file,f,sort_keys=False)
        print("Namespace created succesfully")



