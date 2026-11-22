from datetime import datetime
def build_report(mission,instrument,dataset_name,metadata=None,stats=None):
    lines=["LUNARLENS — OBSERVATION SUMMARY","Generated: "+datetime.now().astimezone().isoformat(timespec="seconds"),
           "",f"Mission: {mission}",f"Instrument: {instrument}",f"Dataset: {dataset_name}","","METADATA"]
    lines += [f"- {k}: {v}" for k,v in (metadata or {}).items()] or ["No metadata loaded."]
    lines += ["","TERRAIN SUMMARY"]+[f"- {k}: {v}" for k,v in (stats or {}).items()] if stats else ["","TERRAIN SUMMARY","No terrain analysis performed."]
    lines += ["","Interpret measurements using official product labels and documentation.",
              "This is an educational exploration aid, not a scientific validation product."]
    return "\n".join(lines)
