from fmiopendata.wfs import download_stored_query
import datetime as dt
import math

bbox = "18,60,32,71"

end_time = dt.datetime.utcnow()
start_time = end_time - dt.timedelta(minutes=20)
start_time = start_time.isoformat(timespec="seconds") + "Z"
end_time = end_time.isoformat(timespec="seconds") + "Z"

def getweather():
    obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=["bbox=" + bbox,
                                  "starttime=" + start_time,
                                  "endtime=" + end_time,
                                  "timeseries=True"])
    tmp_list = []
    for a in obs.data.keys():
        latest = len(obs.data[a]['times'])-1
        if not ( (math.isnan(obs.data[a]["Air temperature"]["values"][latest]))
            and (math.isnan(obs.data[a]["Wind speed"]["values"][latest]))
            and (math.isnan(obs.data[a]["Wind direction"]["values"][latest])) ):
            tmp_list.append({
                'lon' : obs.location_metadata[a]['longitude'],
                'lat' : obs.location_metadata[a]['latitude'],
                'id': obs.location_metadata[a]['fmisid'],
                'name': a,
                'temp': obs.data[a]["Air temperature"]["values"][latest],
                'ws': obs.data[a]["Wind speed"]["values"][latest],
                'wd': obs.data[a]["Wind direction"]["values"][latest]
            })
    return tmp_list

def getextrad():
    obs = download_stored_query("stuk::observations::external-radiation::latest::multipointcoverage",
                            args=["bbox=" + bbox, "timeseries=True"])
    tmp_list = []
    for a in obs.data.keys():
        tmp_list.append({
            'geometry' : Point(obs.location_metadata[a]['longitude'], obs.location_metadata[a]['latitude']),
            'id': obs.location_metadata[a]['fmisid'],
            'name': a,
            'doserate': obs.data[a]["Dose rate"]["values"][0],
            'dr_unit': obs.data[a]["Dose rate"]["unit"],
            'rel_uncert': obs.data[a]["Relative uncertainty"]["values"][0],
            'ru_unit': obs.data[a]["Relative uncertainty"]["unit"],
            'update': obs.data[a]["times"][0].isoformat(timespec="seconds")+ "Z"
        })
    return tmp_list
