# directIO with download

Downloads the whole file in memory and processes this buffer directly. While one
file is being processed the other one is being downloaded in a separate thread.

Uses [requests-futures](https://github.com/ross/requests-futures)

For panda submission a tarball has to be created since extra code is needed on top of the container:

```
tar cfz ../directIO_with_download.tgz *
cd ..
prun --containerImage /cvmfs/unpacked.cern.ch/registry.hub.docker.com/nikolaihartmann/physlite-experiments:6f11b90 \
     --inTarBall=directIO_with_download.tgz \
     --exec="python run_with_download.py '%IN'" \
     --inDS=data17_13TeV.periodK.physics_Main.PhysCont.DAOD_PHYSLITE.grp17_v01_p4309 \
     --outDS=user.nihartma.test_physlite_analysis_GCP_10p_directIO_with_download_preload_2021-05-28_1719 \
     --nFilesPerJob 30 \
     --site=GOOGLE100 \
     --destSE=GOOGLE_EU
```
