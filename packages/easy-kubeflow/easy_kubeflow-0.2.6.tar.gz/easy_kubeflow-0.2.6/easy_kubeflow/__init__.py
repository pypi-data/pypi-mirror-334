from easy_kubeflow._docker import EasyDocker
from easy_kubeflow.submitjobs import EasyJobs, JobSpec, ReuseJobSpec

try:
    from easy_kubeflow.pipelines import Component, ReuseComponent, EasyPipelines
except ImportError as ie:
    print(f"Can not use pipelines when requests-toolbelt>=1")
    print(f"ModuleNotCompatibleError: {ie}")
