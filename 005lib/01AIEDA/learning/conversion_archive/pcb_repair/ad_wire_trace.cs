using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
public class AdTraceRow {
 public string Page, Kind, Name, RefPin, Coordinate, AlternateCoordinate;
 public int Line;
 public bool OriginTouchesWireOrPin, RightTouchesWireOrPin; public string ChosenEndpoint;
 public string[] Pins, Labels, PowerNames;
 public int[] WireLines;
 public string Note;
}
public static class AdWireTrace {
 class Rec { public Dictionary<string,string> D; public int Index,Line; public string G(string k,string f=""){string v;return D.TryGetValue(k,out v)?v:f;} public int I(string k,int f=0){int n;return int.TryParse(G(k),out n)?n:f;} }
 struct Pt {public long X,Y; public Pt(long x,long y){X=x;Y=y;}public string Key(){return X+","+Y;}public override string ToString(){return (X/100000.0).ToString("0.#####")+","+(Y/100000.0).ToString("0.#####");}}
 class Wire {public Rec R; public List<Pt>P=new List<Pt>(); public int Node;}
 class Pin {public Rec R;public Pt P;public int Node;public string Key;}
 class Named {public Rec R;public Pt P;public int Node;public string Name,Kind;}
 class UF {List<int>P=new List<int>();public int New(){P.Add(P.Count);return P.Count-1;}public int Find(int x){while(P[x]!=x){P[x]=P[P[x]];x=P[x];}return x;} public void Join(int a,int b){a=Find(a);b=Find(b);if(a!=b)P[b]=a;}}
 static long C(Rec r,string k){return (long)r.I(k)*100000L+r.I(k+"_FRAC");}
 static Pt Point(Rec r){return new Pt(C(r,"LOCATION.X"),C(r,"LOCATION.Y"));}
 static Pt Hot(Rec r){Pt p=Point(r);long len=(long)r.I("PINLENGTH")*100000L;int o=r.I("PINCONGLOMERATE")&3;if(o==0)p.X+=len;else if(o==1)p.Y+=len;else if(o==2)p.X-=len;else p.Y-=len;return p;}
 static bool Same(Pt a,Pt b){return a.X==b.X&&a.Y==b.Y;}
 static bool On(Pt p,Pt a,Pt b){return (p.X-a.X)*(b.Y-a.Y)==(p.Y-a.Y)*(b.X-a.X)&&p.X>=Math.Min(a.X,b.X)&&p.X<=Math.Max(a.X,b.X)&&p.Y>=Math.Min(a.Y,b.Y)&&p.Y<=Math.Max(a.Y,b.Y);}
 static bool Touch(Pt p,Wire w){for(int i=1;i<w.P.Count;i++)if(On(p,w.P[i-1],w.P[i]))return true;return false;}
 static Rec Read(string l,int idx,int ln){var r=new Rec{D=new Dictionary<string,string>(StringComparer.OrdinalIgnoreCase),Index=idx,Line=ln};foreach(string f in l.Split('|')){int n=f.IndexOf('=');if(n>=0)r.D[f.Substring(0,n)]=f.Substring(n+1);}return r;}
 public static AdTraceRow[] Analyze(string file,string[] wantedNames,string[] wantedPins) {
  var targets=new HashSet<string>(wantedNames,StringComparer.OrdinalIgnoreCase);var pinTargets=new HashSet<string>(wantedPins,StringComparer.OrdinalIgnoreCase);
  var records=new List<Rec>();string[] lines=File.ReadAllLines(file);for(int i=0;i<lines.Length;i++)if(lines[i].StartsWith("|RECORD="))records.Add(Read(lines[i],records.Count,i+1));
  var components=records.Where(r=>r.G("RECORD")=="1").ToDictionary(r=>r.Index,r=>r);var refs=new Dictionary<int,string>();foreach(var r in records)if(r.G("RECORD")=="34"&&r.G("NAME")=="Designator")refs[r.I("OWNERINDEX",-1)]=r.G("TEXT");
  var uf=new UF();var wires=new List<Wire>();var pins=new List<Pin>();var named=new List<Named>();
  foreach(var r in records) {
   string typ=r.G("RECORD");
   if(typ=="27"){var w=new Wire{R=r,Node=uf.New()};for(int i=1;i<=r.I("LOCATIONCOUNT");i++)w.P.Add(new Pt(C(r,"X"+i),C(r,"Y"+i)));wires.Add(w);}
   else if(typ=="2"){Rec comp;string rd;int oi=r.I("OWNERINDEX",-1);if(!components.TryGetValue(oi,out comp)||!refs.TryGetValue(oi,out rd))continue;int owner=r.I("OWNERPARTID",-1);if(owner>0&&owner!=comp.I("CURRENTPARTID",1))continue;pins.Add(new Pin{R=r,P=Hot(r),Node=uf.New(),Key=rd+"|"+r.G("DESIGNATOR")});}
   else if(typ=="17"||typ=="25")named.Add(new Named{R=r,P=Point(r),Node=uf.New(),Name=r.G("TEXT"),Kind=typ=="17"?"POWER":"LABEL"});
  }
  for(int i=0;i<wires.Count;i++)for(int j=i+1;j<wires.Count;j++){bool hit=false;foreach(var p in wires[i].P)if(Touch(p,wires[j])){hit=true;break;}if(!hit)foreach(var p in wires[j].P)if(Touch(p,wires[i])){hit=true;break;}if(hit)uf.Join(wires[i].Node,wires[j].Node);}
  var points=new Dictionary<string,int>();foreach(var p in pins){int old;if(points.TryGetValue(p.P.Key(),out old))uf.Join(p.Node,old);else points[p.P.Key()]=p.Node;foreach(var w in wires)if(Touch(p.P,w))uf.Join(p.Node,w.Node);}
  var sameNames=new Dictionary<string,int>(StringComparer.OrdinalIgnoreCase);foreach(var n in named){int old;if(points.TryGetValue(n.P.Key(),out old))uf.Join(n.Node,old);else points[n.P.Key()]=n.Node;foreach(var w in wires)if(Touch(n.P,w))uf.Join(n.Node,w.Node);string k=n.Kind+":"+n.Name;if(sameNames.TryGetValue(k,out old))uf.Join(n.Node,old);else sameNames[k]=n.Node;}
  var results=new List<AdTraceRow>();string page=Path.GetFileNameWithoutExtension(file);
  Action<AdTraceRow,HashSet<int>> collect=(row,roots)=>{row.Pins=pins.Where(p=>roots.Contains(uf.Find(p.Node))).Select(p=>p.Key).OrderBy(x=>x).ToArray();row.Labels=named.Where(n=>n.Kind=="LABEL"&&roots.Contains(uf.Find(n.Node))).Select(n=>n.Name).Distinct().OrderBy(x=>x).ToArray();row.PowerNames=named.Where(n=>n.Kind=="POWER"&&roots.Contains(uf.Find(n.Node))).Select(n=>n.Name).Distinct().OrderBy(x=>x).ToArray();row.WireLines=wires.Where(w=>roots.Contains(uf.Find(w.Node))).Select(w=>w.R.Line).OrderBy(x=>x).ToArray();};
  foreach(var r in records.Where(r=>r.G("RECORD")=="18"&&targets.Contains(r.G("NAME")))){Pt p=Point(r);Pt p2=new Pt(p.X+(long)r.I("WIDTH")*100000,p.Y);var a=new HashSet<int>();var b=new HashSet<int>();foreach(var w in wires){if(Touch(p,w))a.Add(uf.Find(w.Node));if(Touch(p2,w))b.Add(uf.Find(w.Node));}int old;if(points.TryGetValue(p.Key(),out old))a.Add(uf.Find(old));if(points.TryGetValue(p2.Key(),out old))b.Add(uf.Find(old));var roots=new HashSet<int>(a);roots.UnionWith(b);var row=new AdTraceRow{Page=page,Kind="PORT",Name=r.G("NAME"),Line=r.Line,Coordinate=p.ToString(),AlternateCoordinate=p2.ToString(),Note="Record18: trace both horizontal endpoint candidates; matched roots at location="+a.Count+", at location+width="+b.Count+". If endpoints touch different roots this needs native AD confirmation."};row.OriginTouchesWireOrPin=wires.Any(w=>Touch(p,w))||pins.Any(q=>Same(p,q.P));row.RightTouchesWireOrPin=wires.Any(w=>Touch(p2,w))||pins.Any(q=>Same(p2,q.P));row.ChosenEndpoint=row.OriginTouchesWireOrPin&&!row.RightTouchesWireOrPin?"ORIGIN":!row.OriginTouchesWireOrPin&&row.RightTouchesWireOrPin?"RIGHT":row.OriginTouchesWireOrPin&&row.RightTouchesWireOrPin?(roots.Count==1?"BOTH_SAME_NET":"BOTH_DIFFERENT_NETS_REVIEW"):"NEITHER_REVIEW";collect(row,roots);results.Add(row);}
  foreach(var n in named.Where(n=>targets.Contains(n.Name))){var row=new AdTraceRow{Page=page,Kind=n.Kind,Name=n.Name,Line=n.R.Line,Coordinate=n.P.ToString()};collect(row,new HashSet<int>{uf.Find(n.Node)});results.Add(row);}
  foreach(var p in pins.Where(p=>pinTargets.Contains(p.Key))){var row=new AdTraceRow{Page=page,Kind="PIN",Name=p.R.G("NAME"),RefPin=p.Key,Line=p.R.Line,Coordinate=p.P.ToString()};collect(row,new HashSet<int>{uf.Find(p.Node)});results.Add(row);}
  return results.ToArray();
 }
}
