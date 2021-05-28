# standard setup for copy2scratch

prun --containerImage /cvmfs/unpacked.cern.ch/registry.hub.docker.com/nikolaihartmann/physlite-experiments:latest \
     --exec="python -m physlite_experiments.scripts.run_analysis_example %IN" \
     --inDS=data17_13TeV.periodK.physics_Main.PhysCont.DAOD_PHYSLITE.grp17_v01_p4309 \
     --outDS=user.nihartma.test_physlite_analysis_GCP_10p_copy2scratch_2021-05-27_1328 \
     --nFilesPerJob 30 \
     --site=GOOGLE100 \
     --forceStaged --forceStagedSecondary \
     --destSE=GOOGLE_EU
