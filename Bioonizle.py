from flask import Flask, render_template_string
app = Flask(__name__)

IMW="700px";TH="140px";PW="405px";PMW="255%";PFS="12.9px";PML=3;CL=230

HTML = r'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>FF Bio Editor</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
  min-height:100vh;
  background:#1a1a2e;
  font-family:Arial,sans-serif;
  color:white;
  padding:20px 10px;
  display:flex;
  flex-direction:column;
  align-items:center;
}
h1{
  margin-bottom:20px;
  font-size:1.4em;
  color:#ff8a00;
}
.input-header {
  width:100%;
  max-width:{{ IMW }};
  display:flex;
  justify-content:space-between;
  margin-bottom:8px;
  font-size:14px;
}
textarea{
  width:100%;
  max-width:{{ IMW }};
  height:{{ TH }};
  background:#0d0d0d;
  border:1px solid #333;
  border-radius:10px;
  padding:12px;
  color:#fff;
  font-family:monospace;
  font-size:13px;
  resize:vertical;
  display:block;
}
.preview-wrap {
  width:{{ PW }};
  max-width:{{ PMW }};
  margin-top:30px;
  background:rgba(20,20,25,0.85);
  border:1px solid rgba(255,255,255,0.05);
  border-radius:2px;
  padding:6px 8px;
  font-family:'Arial Narrow','Roboto Condensed','Impact',sans-serif;
  font-size:{{ PFS }};
  font-weight:900;
  line-height:1.15;
  text-shadow:1px 1px 0px #000,0px 0px 2px rgba(0,0,0,0.8);
  letter-spacing:0.3px;
  word-break: normal;
  overflow-wrap: break-word;
  white-space: normal;
  height: calc(1.15em * {{ PML }} + 12px);
  overflow: hidden;
  cursor: pointer;
}
</style>
</head>
<body>
<h1>🔥 FF Bio Editor</h1>

<div class="input-header">
  <span style="color:#ccc;">Bio Kodu:</span>
  <span id="charCount" style="color:#aaa; font-weight:bold;">0 / {{ CL }}</span>
</div>

<textarea id="inp" placeholder="[c][B][00ff00]HEX [ff0000]BOT ..."></textarea>
<div class="preview-wrap" id="preview" title="Kopyalamak için tıkla">Boş</div>

<script>
const HEX=/^[0-9a-fA-F]{6}$/;
const CL={{ CL }};

function parse(v){
  let out="",color=null,bold=false,i=0;
  while(i<v.length){
    if(v[i]==="["){
      let e=v.indexOf("]",i+1);
      if(e!==-1){
        let tag=v.substring(i+1,e);
        let tup=tag.toUpperCase();
        if(tup==="B"){bold=true;i=e+1;continue}
        if(tup==="/B"){bold=false;i=e+1;continue}
        if(tup==="C"){color=null;i=e+1;continue}
        if(tup==="/C"){i=e+1;continue}
        if(HEX.test(tag)){color="#"+tag;i=e+1;continue}
      }
    }
    if(v[i]==="\\"&&v[i+1]==="n"){out+="<br>";i+=2;continue}
    if(v[i]==="\n"){out+="<br>";i++;continue}
    
    let ch=v[i].replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    let s="";
    if(color)s+="color:"+color+";";
    if(bold)s+="font-weight:bold;";
    out+=s?`<span style="${s}">${ch}</span>`:ch;
    i++;
  }
  return out;
}

function render(){
  let val=document.getElementById("inp").value;
  let countEl=document.getElementById("charCount");
  
  countEl.innerText=val.length+" / "+CL;
  countEl.style.color=val.length>CL?"#ff4444":"#aaa";
  
  let toParse=val;
  let overLimit=false;
  if(val.length>CL){
    toParse=val.substring(0,CL);
    overLimit=true;
  }
  
  let outHTML=parse(toParse);
  if(overLimit) outHTML+='<span style="color:white;font-weight:bold;">...</span>';
  
  let previewDiv=document.getElementById("preview");
  previewDiv.innerHTML=outHTML || "Boş";
}

document.getElementById("preview").addEventListener("click", function() {
  const code = document.getElementById("inp").value;
  if(code && code !== "Boş") {
    navigator.clipboard.writeText(code).then(() => {
        alert("Kod Panoya Kopyalandı!");
    });
  }
});

document.getElementById("inp").addEventListener("input",render);
render();
</script>
</body>
</html>'''

@app.route("/bioonizle")
def home():
    return render_template_string(HTML, IMW=IMW, TH=TH, PW=PW, PMW=PMW, PFS=PFS, PML=PML, CL=CL)

if __name__ == "__main__":
    app.run(debug=True)
