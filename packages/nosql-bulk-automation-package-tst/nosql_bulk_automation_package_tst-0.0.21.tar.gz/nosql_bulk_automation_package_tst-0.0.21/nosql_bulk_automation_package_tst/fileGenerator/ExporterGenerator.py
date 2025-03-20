import os
import yaml


from nosql_bulk_automation_package_tst.fileGenerator.QuotaGeneratorNew import QuotaGeneratorNew
from nosql_bulk_automation_package_tst.fileGenerator.NamespaceGenerator import NamespaceGenerator
from nosql_bulk_automation_package_tst.fileGenerator.ArgocdPhase import ArgocdPhase
import nosql_bulk_automation_package_tst.refernce_file_constants as refs


class ExporterGenerator:
    
    def __init__(self):
        print('\n'+40*'#',end='\n\n')
        print("ExporterGenerator")
        print('\n'+40*'#',end='\n\n')
        
    def exporterGenerator(self,datastore,app,paas_name,sec_zone,phase,cid,reg,LZ):
        expId=cid
        p=os.path.abspath(f"../reference/{(datastore.lower())}-exporter/@namespace@-@region@-@phase@-@exporterId@.yaml")
        print(p)
        exp_version=''
        ref_file_path = refs.cb_exporter_ref_file_path
        # ref_file= open(f"../reference/{(datastore.lower())}-exporter/@namespace@-@region@-@phase@-@exporterId@.yaml",'r')
        ref_file= open(ref_file_path,'r')
        ref_file=ref_file.readlines()
        for i in ref_file:
            if 'version' in i and 'version: "1.0"' not in i:
                exp_version=i
                print(i)
        exp_version=(exp_version.replace("version: ","")).strip()
        exp_version=(exp_version.strip("''""\""))
        print((exp_version.strip("''""\"")))
        version=''
        if datastore=='Elasticsearch':
            exp_type='Elasticsearch'
            version=exp_version
            ns='elk'
        elif datastore=="Couchbase":
            exp_type='couchbase'
            ns='couchbase'
            version=exp_version
        else:
            exp_type='mongodb'
            ns='mongodb'
            version=exp_version
        exp_techno=exp_type+'Exporter'
        sourcePath=f'{(datastore.lower())}/az/{LZ}/{reg}-{phase}-{cid}.yaml'
        exp_file={exp_techno:{},f'setup-{(datastore.lower())}-exp-job':{"version": "1.0"}}
        exp_file[exp_techno]['namespace']=f"datastore-{ns}-exp-{app}"
        exp_file[exp_techno]['version']=version
        exp_file[exp_techno]['phase']=phase
        exp_file[exp_techno]['regionShortName']=reg
        exp_file[exp_techno]['exporterId']=expId
        exp_file[exp_techno]['application']=app
        exp_file[exp_techno]['securityZone']=sec_zone
        exp_file[exp_techno]['source']=sourcePath
        exp_file[exp_techno]['mode']={}
        try:
            if paas_name in ["nld10","nld7","nld8","nld9","prd-we-tcp01","prd-we-tcp02","tst-we-cytr01","eus1","eus2","eus3","eus4"]:
                exp_file[exp_techno]['mode']['withCalico']=True
            else:
                exp_file[exp_techno]['mode']['withCalico']=False
        except:
            pass
        if exp_type=='mongodb':
            exp_file[exp_techno]['mode']['withMongoSync']=False
            exp_file[exp_techno]['mode']['withAtlas']=False
            
            
        

        print(yaml.dump(exp_file))
        
        truePhase=ArgocdPhase.get_phase(phase,paas_name.split('-'))
        
        if not os.path.exists(f"dummyInventory/argocd-nosqlpaas-{truePhase}/{truePhase}/az/{paas_name}/{(datastore.lower())}-exporter"):
            os.makedirs(f"dummyInventory/argocd-nosqlpaas-{truePhase}/{truePhase}/az/{paas_name}/{(datastore.lower())}-exporter")
            print("The new exporter directory is created!")
        with open(f"dummyInventory/argocd-nosqlpaas-{truePhase}/{truePhase}/az/{paas_name}/{(datastore.lower())}-exporter/{exp_file[exp_techno]['namespace']}-{reg}-{phase}-{cid}.yaml",'w+') as f:
            yaml.dump(exp_file,f,sort_keys=False)
            print("Exporter created succesfully")
        types='exp'
        if not os.path.exists(f"dummyInventory/argocd-nosqlpaas-{truePhase}/{truePhase}/az/{paas_name}/namespace/{(exp_file[exp_techno]['namespace'])}.yaml"):
            print("Need to create the namespace")
            NamespaceGenerator().namespaceGenerator(datastore,app,paas_name,phase,types)
        else:
            print("Namespace alrady exists")
        
                
        ##generating Quota

        
        if not os.path.exists(f"dummyInventory/argocd-nosqlpaas-{truePhase}/{truePhase}/az/{paas_name}/quota/quota-{ns}.yaml"):
           print("quota need to be created")
        #    QuotaGenerator().quotaGenerator(app,paas_name,phase)
           QuotaGeneratorNew().quotaGenerator(ns,paas_name,phase)
        else:
            print("Quota already exists")


