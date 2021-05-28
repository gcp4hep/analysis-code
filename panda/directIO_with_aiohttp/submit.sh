# directIO with an experimental uproot source that uses aiohttp and 10 persistent connections
# (works a bit better than the uproot default that opens and closes the connection for each chunk)
# see https://gitlab.cern.ch/nihartma/physlite-experiments/-/blob/ea5bf6a795633ebeda044a00e4a2171b0d064a5a/physlite_experiments/io.py
# for implementation

prun --containerImage /cvmfs/unpacked.cern.ch/registry.hub.docker.com/nikolaihartmann/physlite-experiments:6f11b90 \
     --exec="python -m physlite_experiments.scripts.run_analysis_example '%IN' --aiohttp --aio-num-connections 10" \
     --inDS=data17_13TeV.00338183.physics_Main.deriv.DAOD_PHYSLITE.r10258_p3399_p4309_tid22958105_00 \
     --outDS=user.nihartma.test_physlite_analysis_directIO_aiohttp10_GCP_2021-04-30_1334 \
     --nFilesPerJob 10 \
     --site=GOOGLE100 \
     --destSE=GOOGLE_EU \
     --nFiles 10
