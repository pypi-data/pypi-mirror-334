import{a as ie,b as Ye,g as z,u as We,S as Ze,d as k,t as A,i as f,e as G,h as s,s as ve,m as De,k as Qe,l as ot,f as Xe,n as at}from"./index-Bt3FE9-U.js";import{p as O,q as lt,s as Se,t as Ne}from"./index-BYsBiCQK.js";const st=typeof window>"u";function Fe(n){const e={pending:"yellow",success:"green",error:"red",notFound:"purple",redirected:"gray"};return n.isFetching&&n.status==="success"?n.isFetching==="beforeLoad"?"purple":"blue":e[n.status]}function dt(n,e){const i=n.find(r=>r.routeId===e.id);return i?Fe(i):"gray"}function Gt(){const[n,e]=ie(!1);return(st?Ye:z)(()=>{e(!0)}),n}const ct=n=>{const e=Object.getOwnPropertyNames(Object(n)),i=typeof n=="bigint"?`${n.toString()}n`:n;try{return JSON.stringify(i,e)}catch{return"unable to stringify"}};function ut(n,e=[i=>i]){return n.map((i,r)=>[i,r]).sort(([i,r],[g,a])=>{for(const l of e){const d=l(i),u=l(g);if(typeof d>"u"){if(typeof u>"u")continue;return 1}if(d!==u)return d>u?1:-1}return r-a}).map(([i])=>i)}let ft={data:""},vt=n=>typeof window=="object"?((n?n.querySelector("#_goober"):window._goober)||Object.assign((n||document.head).appendChild(document.createElement("style")),{innerHTML:" ",id:"_goober"})).firstChild:n||ft,gt=/(?:([\u0080-\uFFFF\w-%@]+) *:? *([^{;]+?);|([^;}{]*?) *{)|(}\s*)/g,ht=/\/\*[^]*?\*\/|  +/g,Ve=/\n+/g,ne=(n,e)=>{let i="",r="",g="";for(let a in n){let l=n[a];a[0]=="@"?a[1]=="i"?i=a+" "+l+";":r+=a[1]=="f"?ne(l,a):a+"{"+ne(l,a[1]=="k"?"":e)+"}":typeof l=="object"?r+=ne(l,e?e.replace(/([^,])+/g,d=>a.replace(/([^,]*:\S+\([^)]*\))|([^,])+/g,u=>/&/.test(u)?u.replace(/&/g,d):d?d+" "+u:u)):a):l!=null&&(a=/^--/.test(a)?a:a.replace(/[A-Z]/g,"-$&").toLowerCase(),g+=ne.p?ne.p(a,l):a+":"+l+";")}return i+(e&&g?e+"{"+g+"}":g)+r},ee={},et=n=>{if(typeof n=="object"){let e="";for(let i in n)e+=i+et(n[i]);return e}return n},$t=(n,e,i,r,g)=>{let a=et(n),l=ee[a]||(ee[a]=(u=>{let o=0,t=11;for(;o<u.length;)t=101*t+u.charCodeAt(o++)>>>0;return"go"+t})(a));if(!ee[l]){let u=a!==n?n:(o=>{let t,$,p=[{}];for(;t=gt.exec(o.replace(ht,""));)t[4]?p.shift():t[3]?($=t[3].replace(Ve," ").trim(),p.unshift(p[0][$]=p[0][$]||{})):p[0][t[1]]=t[2].replace(Ve," ").trim();return p[0]})(n);ee[l]=ne(g?{["@keyframes "+l]:u}:u,i?"":"."+l)}let d=i&&ee.g?ee.g:null;return i&&(ee.g=ee[l]),((u,o,t,$)=>{$?o.data=o.data.replace($,u):o.data.indexOf(u)===-1&&(o.data=t?u+o.data:o.data+u)})(ee[l],e,r,d),l},bt=(n,e,i)=>n.reduce((r,g,a)=>{let l=e[a];if(l&&l.call){let d=l(i),u=d&&d.props&&d.props.className||/^go/.test(d)&&d;l=u?"."+u:d&&typeof d=="object"?d.props?"":ne(d,""):d===!1?"":d}return r+g+(l??"")},"");function se(n){let e=this||{},i=n.call?n(e.p):n;return $t(i.unshift?i.raw?bt(i,[].slice.call(arguments,1),e.p):i.reduce((r,g)=>Object.assign(r,g&&g.call?g(e.p):g),{}):i,vt(e.target),e.g,e.o,e.k)}se.bind({g:1});se.bind({k:1});const F={colors:{inherit:"inherit",current:"currentColor",transparent:"transparent",black:"#000000",white:"#ffffff",neutral:{50:"#f9fafb",100:"#f2f4f7",200:"#eaecf0",300:"#d0d5dd",400:"#98a2b3",500:"#667085",600:"#475467",700:"#344054",800:"#1d2939",900:"#101828"},darkGray:{50:"#525c7a",100:"#49536e",200:"#414962",300:"#394056",400:"#313749",500:"#292e3d",600:"#212530",700:"#191c24",800:"#111318",900:"#0b0d10"},gray:{50:"#f9fafb",100:"#f2f4f7",200:"#eaecf0",300:"#d0d5dd",400:"#98a2b3",500:"#667085",600:"#475467",700:"#344054",800:"#1d2939",900:"#101828"},blue:{25:"#F5FAFF",50:"#EFF8FF",100:"#D1E9FF",200:"#B2DDFF",300:"#84CAFF",400:"#53B1FD",500:"#2E90FA",600:"#1570EF",700:"#175CD3",800:"#1849A9",900:"#194185"},green:{25:"#F6FEF9",50:"#ECFDF3",100:"#D1FADF",200:"#A6F4C5",300:"#6CE9A6",400:"#32D583",500:"#12B76A",600:"#039855",700:"#027A48",800:"#05603A",900:"#054F31"},red:{50:"#fef2f2",100:"#fee2e2",200:"#fecaca",300:"#fca5a5",400:"#f87171",500:"#ef4444",600:"#dc2626",700:"#b91c1c",800:"#991b1b",900:"#7f1d1d",950:"#450a0a"},yellow:{25:"#FFFCF5",50:"#FFFAEB",100:"#FEF0C7",200:"#FEDF89",300:"#FEC84B",400:"#FDB022",500:"#F79009",600:"#DC6803",700:"#B54708",800:"#93370D",900:"#7A2E0E"},purple:{25:"#FAFAFF",50:"#F4F3FF",100:"#EBE9FE",200:"#D9D6FE",300:"#BDB4FE",400:"#9B8AFB",500:"#7A5AF8",600:"#6938EF",700:"#5925DC",800:"#4A1FB8",900:"#3E1C96"},teal:{25:"#F6FEFC",50:"#F0FDF9",100:"#CCFBEF",200:"#99F6E0",300:"#5FE9D0",400:"#2ED3B7",500:"#15B79E",600:"#0E9384",700:"#107569",800:"#125D56",900:"#134E48"},pink:{25:"#fdf2f8",50:"#fce7f3",100:"#fbcfe8",200:"#f9a8d4",300:"#f472b6",400:"#ec4899",500:"#db2777",600:"#be185d",700:"#9d174d",800:"#831843",900:"#500724"},cyan:{25:"#ecfeff",50:"#cffafe",100:"#a5f3fc",200:"#67e8f9",300:"#22d3ee",400:"#06b6d4",500:"#0891b2",600:"#0e7490",700:"#155e75",800:"#164e63",900:"#083344"}},alpha:{90:"e5",70:"b3",20:"33"},font:{size:{"2xs":"calc(var(--tsrd-font-size) * 0.625)",xs:"calc(var(--tsrd-font-size) * 0.75)",sm:"calc(var(--tsrd-font-size) * 0.875)",md:"var(--tsrd-font-size)"},lineHeight:{xs:"calc(var(--tsrd-font-size) * 1)",sm:"calc(var(--tsrd-font-size) * 1.25)"},weight:{normal:"400",medium:"500",semibold:"600",bold:"700"},fontFamily:{sans:"ui-sans-serif, Inter, system-ui, sans-serif, sans-serif",mono:"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"}},border:{radius:{xs:"calc(var(--tsrd-font-size) * 0.125)",sm:"calc(var(--tsrd-font-size) * 0.25)",md:"calc(var(--tsrd-font-size) * 0.375)",full:"9999px"}},size:{0:"0px",.5:"calc(var(--tsrd-font-size) * 0.125)",1:"calc(var(--tsrd-font-size) * 0.25)",1.5:"calc(var(--tsrd-font-size) * 0.375)",2:"calc(var(--tsrd-font-size) * 0.5)",2.5:"calc(var(--tsrd-font-size) * 0.625)",3:"calc(var(--tsrd-font-size) * 0.75)",3.5:"calc(var(--tsrd-font-size) * 0.875)",4:"calc(var(--tsrd-font-size) * 1)",5:"calc(var(--tsrd-font-size) * 1.25)",8:"calc(var(--tsrd-font-size) * 2)"}},mt=n=>{const{colors:e,font:i,size:r,alpha:g,border:a}=F,{fontFamily:l,lineHeight:d,size:u}=i,o=n?se.bind({target:n}):se;return{devtoolsPanelContainer:o`
      direction: ltr;
      position: fixed;
      bottom: 0;
      right: 0;
      z-index: 99999;
      width: 100%;
      max-height: 90%;
      border-top: 1px solid ${e.gray[700]};
      transform-origin: top;
    `,devtoolsPanelContainerVisibility:t=>o`
        visibility: ${t?"visible":"hidden"};
      `,devtoolsPanelContainerResizing:t=>t()?o`
          transition: none;
        `:o`
        transition: all 0.4s ease;
      `,devtoolsPanelContainerAnimation:(t,$)=>t?o`
          pointer-events: auto;
          transform: translateY(0);
        `:o`
        pointer-events: none;
        transform: translateY(${$}px);
      `,logo:o`
      cursor: pointer;
      display: flex;
      flex-direction: column;
      background-color: transparent;
      border: none;
      font-family: ${l.sans};
      gap: ${F.size[.5]};
      padding: 0px;
      &:hover {
        opacity: 0.7;
      }
      &:focus-visible {
        outline-offset: 4px;
        border-radius: ${a.radius.xs};
        outline: 2px solid ${e.blue[800]};
      }
    `,tanstackLogo:o`
      font-size: ${i.size.md};
      font-weight: ${i.weight.bold};
      line-height: ${i.lineHeight.xs};
      white-space: nowrap;
      color: ${e.gray[300]};
    `,routerLogo:o`
      font-weight: ${i.weight.semibold};
      font-size: ${i.size.xs};
      background: linear-gradient(to right, #84cc16, #10b981);
      background-clip: text;
      -webkit-background-clip: text;
      line-height: 1;
      -webkit-text-fill-color: transparent;
      white-space: nowrap;
    `,devtoolsPanel:o`
      display: flex;
      font-size: ${u.sm};
      font-family: ${l.sans};
      background-color: ${e.darkGray[700]};
      color: ${e.gray[300]};

      @media (max-width: 700px) {
        flex-direction: column;
      }
      @media (max-width: 600px) {
        font-size: ${u.xs};
      }
    `,dragHandle:o`
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 4px;
      cursor: row-resize;
      z-index: 100000;
      &:hover {
        background-color: ${e.purple[400]}${g[90]};
      }
    `,firstContainer:o`
      flex: 1 1 500px;
      min-height: 40%;
      max-height: 100%;
      overflow: auto;
      border-right: 1px solid ${e.gray[700]};
      display: flex;
      flex-direction: column;
    `,routerExplorerContainer:o`
      overflow-y: auto;
      flex: 1;
    `,routerExplorer:o`
      padding: ${F.size[2]};
    `,row:o`
      display: flex;
      align-items: center;
      padding: ${F.size[2]} ${F.size[2.5]};
      gap: ${F.size[2.5]};
      border-bottom: ${e.darkGray[500]} 1px solid;
      align-items: center;
    `,detailsHeader:o`
      font-family: ui-sans-serif, Inter, system-ui, sans-serif, sans-serif;
      position: sticky;
      top: 0;
      z-index: 2;
      background-color: ${e.darkGray[600]};
      padding: 0px ${F.size[2]};
      font-weight: ${i.weight.medium};
      font-size: ${i.size.xs};
      min-height: ${F.size[8]};
      line-height: ${i.lineHeight.xs};
      text-align: left;
      display: flex;
      align-items: center;
    `,maskedBadge:o`
      background: ${e.yellow[900]}${g[70]};
      color: ${e.yellow[300]};
      display: inline-block;
      padding: ${F.size[0]} ${F.size[2.5]};
      border-radius: ${a.radius.full};
      font-size: ${i.size.xs};
      font-weight: ${i.weight.normal};
      border: 1px solid ${e.yellow[300]};
    `,maskedLocation:o`
      color: ${e.yellow[300]};
    `,detailsContent:o`
      padding: ${F.size[1.5]} ${F.size[2]};
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: ${i.size.xs};
    `,routeMatchesToggle:o`
      display: flex;
      align-items: center;
      border: 1px solid ${e.gray[500]};
      border-radius: ${a.radius.sm};
      overflow: hidden;
    `,routeMatchesToggleBtn:(t,$)=>{const y=[o`
        appearance: none;
        border: none;
        font-size: 12px;
        padding: 4px 8px;
        background: transparent;
        cursor: pointer;
        font-family: ${l.sans};
        font-weight: ${i.weight.medium};
      `];if(t){const T=o`
          background: ${e.darkGray[400]};
          color: ${e.gray[300]};
        `;y.push(T)}else{const T=o`
          color: ${e.gray[500]};
          background: ${e.darkGray[800]}${g[20]};
        `;y.push(T)}return $&&y.push(o`
          border-right: 1px solid ${F.colors.gray[500]};
        `),y},detailsHeaderInfo:o`
      flex: 1;
      justify-content: flex-end;
      display: flex;
      align-items: center;
      font-weight: ${i.weight.normal};
      color: ${e.gray[400]};
    `,matchRow:t=>{const p=[o`
        display: flex;
        border-bottom: 1px solid ${e.darkGray[400]};
        cursor: pointer;
        align-items: center;
        padding: ${r[1]} ${r[2]};
        gap: ${r[2]};
        font-size: ${u.xs};
        color: ${e.gray[300]};
      `];if(t){const y=o`
          background: ${e.darkGray[500]};
        `;p.push(y)}return p},matchIndicator:t=>{const p=[o`
        flex: 0 0 auto;
        width: ${r[3]};
        height: ${r[3]};
        background: ${e[t][900]};
        border: 1px solid ${e[t][500]};
        border-radius: ${a.radius.full};
        transition: all 0.25s ease-out;
        box-sizing: border-box;
      `];if(t==="gray"){const y=o`
          background: ${e.gray[700]};
          border-color: ${e.gray[400]};
        `;p.push(y)}return p},matchID:o`
      flex: 1;
      line-height: ${d.xs};
    `,ageTicker:t=>{const p=[o`
        display: flex;
        gap: ${r[1]};
        font-size: ${u.xs};
        color: ${e.gray[400]};
        font-variant-numeric: tabular-nums;
        line-height: ${d.xs};
      `];if(t){const y=o`
          color: ${e.yellow[400]};
        `;p.push(y)}return p},secondContainer:o`
      flex: 1 1 500px;
      min-height: 40%;
      max-height: 100%;
      overflow: auto;
      border-right: 1px solid ${e.gray[700]};
      display: flex;
      flex-direction: column;
    `,thirdContainer:o`
      flex: 1 1 500px;
      overflow: auto;
      display: flex;
      flex-direction: column;
      height: 100%;
      border-right: 1px solid ${e.gray[700]};

      @media (max-width: 700px) {
        border-top: 2px solid ${e.gray[700]};
      }
    `,fourthContainer:o`
      flex: 1 1 500px;
      min-height: 40%;
      max-height: 100%;
      overflow: auto;
      display: flex;
      flex-direction: column;
    `,routesContainer:o`
      overflow-x: auto;
      overflow-y: visible;
    `,routesRowContainer:(t,$)=>{const y=[o`
        display: flex;
        border-bottom: 1px solid ${e.darkGray[400]};
        align-items: center;
        padding: ${r[1]} ${r[2]};
        gap: ${r[2]};
        font-size: ${u.xs};
        color: ${e.gray[300]};
        cursor: ${$?"pointer":"default"};
        line-height: ${d.xs};
      `];if(t){const T=o`
          background: ${e.darkGray[500]};
        `;y.push(T)}return y},routesRow:t=>{const p=[o`
        flex: 1 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: ${u.xs};
        line-height: ${d.xs};
      `];if(!t){const y=o`
          color: ${e.gray[400]};
        `;p.push(y)}return p},routeParamInfo:o`
      color: ${e.gray[400]};
      font-size: ${u.xs};
      line-height: ${d.xs};
    `,nestedRouteRow:t=>o`
        margin-left: ${t?0:r[3.5]};
        border-left: ${t?"":`solid 1px ${e.gray[700]}`};
      `,code:o`
      font-size: ${u.xs};
      line-height: ${d.xs};
    `,matchesContainer:o`
      flex: 1 1 auto;
      overflow-y: auto;
    `,cachedMatchesContainer:o`
      flex: 1 1 auto;
      overflow-y: auto;
      max-height: 50%;
    `,maskedBadgeContainer:o`
      flex: 1;
      justify-content: flex-end;
      display: flex;
    `,matchDetails:o`
      display: flex;
      flex-direction: column;
      padding: ${F.size[2]};
      font-size: ${F.font.size.xs};
      color: ${F.colors.gray[300]};
      line-height: ${F.font.lineHeight.sm};
    `,matchStatus:(t,$)=>{const y=$&&t==="success"?$==="beforeLoad"?"purple":"blue":{pending:"yellow",success:"green",error:"red",notFound:"purple",redirected:"gray"}[t];return o`
        display: flex;
        justify-content: center;
        align-items: center;
        height: 40px;
        border-radius: ${F.border.radius.sm};
        font-weight: ${F.font.weight.normal};
        background-color: ${F.colors[y][900]}${F.alpha[90]};
        color: ${F.colors[y][300]};
        border: 1px solid ${F.colors[y][600]};
        margin-bottom: ${F.size[2]};
        transition: all 0.25s ease-out;
      `},matchDetailsInfo:o`
      display: flex;
      justify-content: flex-end;
      flex: 1;
    `,matchDetailsInfoLabel:o`
      display: flex;
    `,mainCloseBtn:o`
      background: ${e.darkGray[700]};
      padding: ${r[1]} ${r[2]} ${r[1]} ${r[1.5]};
      border-radius: ${a.radius.md};
      position: fixed;
      z-index: 99999;
      display: inline-flex;
      width: fit-content;
      cursor: pointer;
      appearance: none;
      border: 0;
      gap: 8px;
      align-items: center;
      border: 1px solid ${e.gray[500]};
      font-size: ${i.size.xs};
      cursor: pointer;
      transition: all 0.25s ease-out;

      &:hover {
        background: ${e.darkGray[500]};
      }
    `,mainCloseBtnPosition:t=>o`
        ${t==="top-left"?`top: ${r[2]}; left: ${r[2]};`:""}
        ${t==="top-right"?`top: ${r[2]}; right: ${r[2]};`:""}
        ${t==="bottom-left"?`bottom: ${r[2]}; left: ${r[2]};`:""}
        ${t==="bottom-right"?`bottom: ${r[2]}; right: ${r[2]};`:""}
      `,mainCloseBtnAnimation:t=>t?o`
        opacity: 0;
        pointer-events: none;
        visibility: hidden;
      `:o`
          opacity: 1;
          pointer-events: auto;
          visibility: visible;
        `,routerLogoCloseButton:o`
      font-weight: ${i.weight.semibold};
      font-size: ${i.size.xs};
      background: linear-gradient(to right, #98f30c, #00f4a3);
      background-clip: text;
      -webkit-background-clip: text;
      line-height: 1;
      -webkit-text-fill-color: transparent;
      white-space: nowrap;
    `,mainCloseBtnDivider:o`
      width: 1px;
      background: ${F.colors.gray[600]};
      height: 100%;
      border-radius: 999999px;
      color: transparent;
    `,mainCloseBtnIconContainer:o`
      position: relative;
      width: ${r[5]};
      height: ${r[5]};
      background: pink;
      border-radius: 999999px;
      overflow: hidden;
    `,mainCloseBtnIconOuter:o`
      width: ${r[5]};
      height: ${r[5]};
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      filter: blur(3px) saturate(1.8) contrast(2);
    `,mainCloseBtnIconInner:o`
      width: ${r[4]};
      height: ${r[4]};
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    `,panelCloseBtn:o`
      position: absolute;
      cursor: pointer;
      z-index: 100001;
      display: flex;
      align-items: center;
      justify-content: center;
      outline: none;
      background-color: ${e.darkGray[700]};
      &:hover {
        background-color: ${e.darkGray[500]};
      }

      top: 0;
      right: ${r[2]};
      transform: translate(0, -100%);
      border-right: ${e.darkGray[300]} 1px solid;
      border-left: ${e.darkGray[300]} 1px solid;
      border-top: ${e.darkGray[300]} 1px solid;
      border-bottom: none;
      border-radius: ${a.radius.sm} ${a.radius.sm} 0px 0px;
      padding: ${r[1]} ${r[1.5]} ${r[.5]} ${r[1.5]};

      &::after {
        content: ' ';
        position: absolute;
        top: 100%;
        left: -${r[2.5]};
        height: ${r[1.5]};
        width: calc(100% + ${r[5]});
      }
    `,panelCloseBtnIcon:o`
      color: ${e.gray[400]};
      width: ${r[2]};
      height: ${r[2]};
    `}};function ye(){const n=We(Ze),[e]=ie(mt(n));return e}const pt=n=>{try{const e=localStorage.getItem(n);return typeof e=="string"?JSON.parse(e):void 0}catch{return}};function Je(n,e){const[i,r]=ie();return Ye(()=>{const a=pt(n);r(typeof a>"u"||a===null?typeof e=="function"?e():e:a)}),[i,a=>{r(l=>{let d=a;typeof a=="function"&&(d=a(l));try{localStorage.setItem(n,JSON.stringify(d))}catch{}return d})}]}var xt=A('<span><svg xmlns=http://www.w3.org/2000/svg width=12 height=12 fill=none viewBox="0 0 24 24"><path stroke=currentColor stroke-linecap=round stroke-linejoin=round stroke-width=2 d="M9 18l6-6-6-6">'),pe=A("<div>"),yt=A("<button><span> "),wt=A("<div><div><button> [<!> ... <!>]"),Ct=A("<button><span></span> 🔄 "),kt=A("<span>:"),_t=A("<span>");const qe=({expanded:n,style:e={}})=>{const i=tt();return(()=>{var r=xt(),g=r.firstChild;return z(a=>{var l=i().expander,d=O(i().expanderIcon(n));return l!==a.e&&s(r,a.e=l),d!==a.t&&ve(g,"class",a.t=d),a},{e:void 0,t:void 0}),r})()};function St(n,e){if(e<1)return[];let i=0;const r=[];for(;i<n.length;)r.push(n.slice(i,i+e)),i=i+e;return r}function Ft(n){return Symbol.iterator in n}function le({value:n,defaultExpanded:e,pageSize:i=100,filterSubEntries:r,...g}){const[a,l]=ie(!!e),d=()=>l(v=>!v),u=k(()=>typeof n()),o=k(()=>{let v=[];const L=b=>{const h=e===!0?{[b.label]:!0}:e==null?void 0:e[b.label];return{...b,value:()=>b.value,defaultExpanded:h}};return Array.isArray(n())?v=n().map((b,h)=>L({label:h.toString(),value:b})):n()!==null&&typeof n()=="object"&&Ft(n())&&typeof n()[Symbol.iterator]=="function"?v=Array.from(n(),(b,h)=>L({label:h.toString(),value:b})):typeof n()=="object"&&n()!==null&&(v=Object.entries(n()).map(([b,h])=>L({label:b,value:h}))),r?r(v):v}),t=k(()=>St(o(),i)),[$,p]=ie([]),[y,T]=ie(void 0),P=tt(),Q=()=>{T(n()())},X=v=>G(le,De({value:n,filterSubEntries:r},g,v));return(()=>{var v=pe();return f(v,(()=>{var L=k(()=>!!t().length);return()=>L()?[(()=>{var b=yt(),h=b.firstChild,E=h.firstChild;return b.$$click=()=>d(),f(b,G(qe,{get expanded(){return a()??!1}}),h),f(b,()=>g.label,h),f(h,()=>String(u).toLowerCase()==="iterable"?"(Iterable) ":"",E),f(h,()=>o().length,E),f(h,()=>o().length>1?"items":"item",null),z(N=>{var K=P().expandButton,_=P().info;return K!==N.e&&s(b,N.e=K),_!==N.t&&s(h,N.t=_),N},{e:void 0,t:void 0}),b})(),k(()=>k(()=>!!(a()??!1))()?k(()=>t().length===1)()?(()=>{var b=pe();return f(b,()=>o().map((h,E)=>X(h))),z(()=>s(b,P().subEntries)),b})():(()=>{var b=pe();return f(b,()=>t().map((h,E)=>(()=>{var N=wt(),K=N.firstChild,_=K.firstChild,V=_.firstChild,ge=V.nextSibling,de=ge.nextSibling,oe=de.nextSibling;return oe.nextSibling,_.$$click=()=>p(H=>H.includes(E)?H.filter(U=>U!==E):[...H,E]),f(_,G(qe,{get expanded(){return $().includes(E)}}),V),f(_,E*i,ge),f(_,E*i+i-1,oe),f(K,(()=>{var H=k(()=>!!$().includes(E));return()=>H()?(()=>{var U=pe();return f(U,()=>h.map(te=>X(te))),z(()=>s(U,P().subEntries)),U})():null})(),null),z(H=>{var U=P().entry,te=O(P().labelButton,"labelButton");return U!==H.e&&s(K,H.e=U),te!==H.t&&s(_,H.t=te),H},{e:void 0,t:void 0}),N})())),z(()=>s(b,P().subEntries)),b})():null)]:(()=>{var b=k(()=>u()==="function");return()=>b()?G(le,{get label(){return(()=>{var h=Ct(),E=h.firstChild;return h.$$click=Q,f(E,()=>g.label),z(()=>s(h,P().refreshValueBtn)),h})()},value:y,defaultExpanded:{}}):[(()=>{var h=kt(),E=h.firstChild;return f(h,()=>g.label,E),h})()," ",(()=>{var h=_t();return f(h,()=>ct(n())),z(()=>s(h,P().value)),h})()]})()})()),z(()=>s(v,P().entry)),v})()}const zt=n=>{const{colors:e,font:i,size:r}=F,{fontFamily:g,lineHeight:a,size:l}=i,d=n?se.bind({target:n}):se;return{entry:d`
      font-family: ${g.mono};
      font-size: ${l.xs};
      line-height: ${a.sm};
      outline: none;
      word-break: break-word;
    `,labelButton:d`
      cursor: pointer;
      color: inherit;
      font: inherit;
      outline: inherit;
      background: transparent;
      border: none;
      padding: 0;
    `,expander:d`
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: ${r[3]};
      height: ${r[3]};
      padding-left: 3px;
      box-sizing: content-box;
    `,expanderIcon:u=>u?d`
          transform: rotate(90deg);
          transition: transform 0.1s ease;
        `:d`
        transform: rotate(0deg);
        transition: transform 0.1s ease;
      `,expandButton:d`
      display: flex;
      gap: ${r[1]};
      align-items: center;
      cursor: pointer;
      color: inherit;
      font: inherit;
      outline: inherit;
      background: transparent;
      border: none;
      padding: 0;
    `,value:d`
      color: ${e.purple[400]};
    `,subEntries:d`
      margin-left: ${r[2]};
      padding-left: ${r[2]};
      border-left: 2px solid ${e.darkGray[400]};
    `,info:d`
      color: ${e.gray[500]};
      font-size: ${l["2xs"]};
      padding-left: ${r[1]};
    `,refreshValueBtn:d`
      appearance: none;
      border: 0;
      cursor: pointer;
      background: transparent;
      color: inherit;
      padding: 0;
      font-family: ${g.mono};
      font-size: ${l.xs};
    `}};function tt(){const n=We(Ze),[e]=ie(zt(n));return e}Qe(["click"]);var Dt=A("<div><div></div><div>/</div><div></div><div>/</div><div>");function _e(n){const e=["s","min","h","d"],i=[n/1e3,n/6e4,n/36e5,n/864e5];let r=0;for(let a=1;a<i.length&&!(i[a]<1);a++)r=a;return new Intl.NumberFormat(navigator.language,{compactDisplay:"short",notation:"compact",maximumFractionDigits:0}).format(i[r])+e[r]}function ze({match:n,router:e}){const i=ye();if(!n)return null;const r=e().looseRoutesById[n.routeId];if(!r.options.loader)return null;const g=Date.now()-n.updatedAt,a=r.options.staleTime??e().options.defaultStaleTime??0,l=r.options.gcTime??e().options.defaultGcTime??30*60*1e3;return(()=>{var d=Dt(),u=d.firstChild,o=u.nextSibling,t=o.nextSibling,$=t.nextSibling,p=$.nextSibling;return f(u,()=>_e(g)),f(t,()=>_e(a)),f(p,()=>_e(l)),z(()=>s(d,O(i().ageTicker(g>a)))),d})()}var Et=A("<button><div>TANSTACK</div><div>TanStack Router v1"),Bt=A("<div><div role=button><div></div><div><div><code> </code><code>"),xe=A("<div>"),It=A('<div><button><svg xmlns=http://www.w3.org/2000/svg width=10 height=6 fill=none viewBox="0 0 10 6"><path stroke=currentColor stroke-linecap=round stroke-linejoin=round stroke-width=1.667 d="M1 1l4 4 4-4"></path></svg></button><div><div></div><div><div></div></div></div><div><div><div><span>Pathname</span></div><div><code></code></div><div><div><button type=button>Routes</button><button type=button>Matches</button></div><div><div>age / staleTime / gcTime</div></div></div><div>'),Mt=A("<div><span>masked"),At=A("<code>"),Ke=A("<div role=button><div></div><code>"),Tt=A("<div><div><div>Cached Matches</div><div>age / staleTime / gcTime</div></div><div>"),Pt=A("<div><div>Match Details</div><div><div><div><div></div></div><div><div>ID:</div><div><code></code></div></div><div><div>State:</div><div></div></div><div><div>Last Updated:</div><div></div></div></div></div><div>Explorer</div><div>"),Lt=A("<div>Loader Data"),Rt=A("<div><div>Search Params</div><div>");function jt(n){const{className:e,...i}=n,r=ye();return(()=>{var g=Et(),a=g.firstChild,l=a.nextSibling;return Xe(g,De(i,{get class(){return O(r().logo,e?e():"")}}),!1,!0),z(d=>{var u=r().tanstackLogo,o=r().routerLogo;return u!==d.e&&s(a,d.e=u),o!==d.t&&s(l,d.t=o),d},{e:void 0,t:void 0}),g})()}function rt({routerState:n,router:e,route:i,isRoot:r,activeId:g,setActiveId:a}){const l=ye(),d=k(()=>n().pendingMatches||n().matches),u=k(()=>n().matches.find(t=>t.routeId===i.id)),o=k(()=>{var t,$;try{if((t=u())!=null&&t.params){const p=($=u())==null?void 0:$.params,y=i.path||Ne(i.id);if(y.startsWith("$")){const T=y.slice(1);if(p[T])return`(${p[T]})`}}return""}catch{return""}});return(()=>{var t=Bt(),$=t.firstChild,p=$.firstChild,y=p.nextSibling,T=y.firstChild,P=T.firstChild,Q=P.firstChild,X=P.nextSibling;return $.$$click=()=>{u()&&a(g()===i.id?"":i.id)},f(P,()=>r?Se:i.path||Ne(i.id),Q),f(X,o),f(y,G(ze,{get match(){return u()},router:e}),null),f(t,(()=>{var v=k(()=>{var L;return!!((L=i.children)!=null&&L.length)});return()=>v()?(()=>{var L=xe();return f(L,()=>[...i.children].sort((b,h)=>b.rank-h.rank).map(b=>G(rt,{routerState:n,router:e,route:b,activeId:g,setActiveId:a}))),z(()=>s(L,l().nestedRouteRow(!!r))),L})():null})(),null),z(v=>{var L=`Open match details for ${i.id}`,b=O(l().routesRowContainer(i.id===g(),!!u())),h=O(l().matchIndicator(dt(d(),i))),E=O(l().routesRow(!!u())),N=l().code,K=l().routeParamInfo;return L!==v.e&&ve($,"aria-label",v.e=L),b!==v.t&&s($,v.t=b),h!==v.a&&s(p,v.a=h),E!==v.o&&s(y,v.o=E),N!==v.i&&s(P,v.i=N),K!==v.n&&s(X,v.n=K),v},{e:void 0,t:void 0,a:void 0,o:void 0,i:void 0,n:void 0}),t})()}const Ue=function({...e}){const{isOpen:i=!0,setIsOpen:r,handleDragStart:g,router:a,routerState:l,shadowDOMTarget:d,...u}=e,{onCloseClick:o}=ot(),t=ye(),{className:$,style:p,...y}=u;lt(a,"No router was found for the TanStack Router Devtools. Please place the devtools in the <RouterProvider> component tree or pass the router instance to the devtools manually.");const[T,P]=Je("tanstackRouterDevtoolsShowMatches",!0),[Q,X]=Je("tanstackRouterDevtoolsActiveRouteId",""),v=k(()=>[...l().pendingMatches??[],...l().matches,...l().cachedMatches].find(V=>V.routeId===Q()||V.id===Q())),L=k(()=>Object.keys(l().location.search).length),b=k(()=>({...a(),state:l()})),h=k(()=>Object.fromEntries(ut(Object.keys(b()),["state","routesById","routesByPath","flatRoutes","options","manifest"].map(_=>V=>V!==_)).map(_=>[_,b()[_]]).filter(_=>typeof _[1]!="function"&&!["__store","basepath","injectedHtml","subscribers","latestLoadPromise","navigateTimeout","resetNextScroll","tempLocationKey","latestLocation","routeTree","history"].includes(_[0])))),E=k(()=>{var _;return(_=v())==null?void 0:_.loaderData}),N=k(()=>v()),K=k(()=>l().location.search);return(()=>{var _=It(),V=_.firstChild,ge=V.firstChild,de=V.nextSibling,oe=de.firstChild,H=oe.nextSibling,U=H.firstChild,te=de.nextSibling,Ee=te.firstChild,he=Ee.firstChild;he.firstChild;var $e=he.nextSibling,nt=$e.firstChild,we=$e.nextSibling,Ce=we.firstChild,be=Ce.firstChild,ke=be.nextSibling,it=Ce.nextSibling,Be=we.nextSibling;return Xe(_,De({get class(){return O(t().devtoolsPanel,"TanStackRouterDevtoolsPanel",$?$():"")},get style(){return p?p():""}},y),!1,!0),f(_,g?(()=>{var c=xe();return at(c,"mousedown",g,!0),z(()=>s(c,t().dragHandle)),c})():null,V),V.$$click=c=>{r&&r(!1),o(c)},f(oe,G(jt,{"aria-hidden":!0,onClick:c=>{r&&r(!1),o(c)}})),f(U,G(le,{label:"Router",value:h,defaultExpanded:{state:{},context:{},options:{}},filterSubEntries:c=>c.filter(x=>typeof x.value()!="function")})),f(he,(()=>{var c=k(()=>!!l().location.maskedLocation);return()=>c()?(()=>{var x=Mt(),I=x.firstChild;return z(M=>{var w=t().maskedBadgeContainer,R=t().maskedBadge;return w!==M.e&&s(x,M.e=w),R!==M.t&&s(I,M.t=R),M},{e:void 0,t:void 0}),x})():null})(),null),f(nt,()=>l().location.pathname),f($e,(()=>{var c=k(()=>!!l().location.maskedLocation);return()=>c()?(()=>{var x=At();return f(x,()=>{var I;return(I=l().location.maskedLocation)==null?void 0:I.pathname}),z(()=>s(x,t().maskedLocation)),x})():null})(),null),be.$$click=()=>{P(!1)},ke.$$click=()=>{P(!0)},f(Be,(()=>{var c=k(()=>!T());return()=>c()?G(rt,{routerState:l,router:a,get route(){return a().routeTree},isRoot:!0,activeId:Q,setActiveId:X}):(()=>{var x=xe();return f(x,()=>{var I,M;return(M=(I=l().pendingMatches)!=null&&I.length?l().pendingMatches:l().matches)==null?void 0:M.map((w,R)=>(()=>{var C=Ke(),D=C.firstChild,J=D.nextSibling;return C.$$click=()=>X(Q()===w.id?"":w.id),f(J,()=>`${w.routeId===Se?Se:w.pathname}`),f(C,G(ze,{match:w,router:a}),null),z(B=>{var j=`Open match details for ${w.id}`,q=O(t().matchRow(w===v())),W=O(t().matchIndicator(Fe(w))),Y=t().matchID;return j!==B.e&&ve(C,"aria-label",B.e=j),q!==B.t&&s(C,B.t=q),W!==B.a&&s(D,B.a=W),Y!==B.o&&s(J,B.o=Y),B},{e:void 0,t:void 0,a:void 0,o:void 0}),C})())}),x})()})()),f(te,(()=>{var c=k(()=>!!l().cachedMatches.length);return()=>c()?(()=>{var x=Tt(),I=x.firstChild,M=I.firstChild,w=M.nextSibling,R=I.nextSibling;return f(R,()=>l().cachedMatches.map(C=>(()=>{var D=Ke(),J=D.firstChild,B=J.nextSibling;return D.$$click=()=>X(Q()===C.id?"":C.id),f(B,()=>`${C.id}`),f(D,G(ze,{match:C,router:a}),null),z(j=>{var q=`Open match details for ${C.id}`,W=O(t().matchRow(C===v())),Y=O(t().matchIndicator(Fe(C))),re=t().matchID;return q!==j.e&&ve(D,"aria-label",j.e=q),W!==j.t&&s(D,j.t=W),Y!==j.a&&s(J,j.a=Y),re!==j.o&&s(B,j.o=re),j},{e:void 0,t:void 0,a:void 0,o:void 0}),D})())),z(C=>{var D=t().cachedMatchesContainer,J=t().detailsHeader,B=t().detailsHeaderInfo;return D!==C.e&&s(x,C.e=D),J!==C.t&&s(I,C.t=J),B!==C.a&&s(w,C.a=B),C},{e:void 0,t:void 0,a:void 0}),x})():null})(),null),f(_,(()=>{var c=k(()=>{var x;return!!(v()&&((x=v())!=null&&x.status))});return()=>c()?(()=>{var x=Pt(),I=x.firstChild,M=I.nextSibling,w=M.firstChild,R=w.firstChild,C=R.firstChild,D=R.nextSibling,J=D.firstChild,B=J.nextSibling,j=B.firstChild,q=D.nextSibling,W=q.firstChild,Y=W.nextSibling,re=q.nextSibling,me=re.firstChild,ce=me.nextSibling,ae=M.nextSibling,ue=ae.nextSibling;return f(C,(()=>{var m=k(()=>{var S,Z;return!!(((S=v())==null?void 0:S.status)==="success"&&((Z=v())!=null&&Z.isFetching))});return()=>{var S;return m()?"fetching":(S=v())==null?void 0:S.status}})()),f(j,()=>{var m;return(m=v())==null?void 0:m.id}),f(Y,(()=>{var m=k(()=>{var S;return!!((S=l().pendingMatches)!=null&&S.find(Z=>{var fe;return Z.id===((fe=v())==null?void 0:fe.id)}))});return()=>m()?"Pending":l().matches.find(S=>{var Z;return S.id===((Z=v())==null?void 0:Z.id)})?"Active":"Cached"})()),f(ce,(()=>{var m=k(()=>{var S;return!!((S=v())!=null&&S.updatedAt)});return()=>{var S;return m()?new Date((S=v())==null?void 0:S.updatedAt).toLocaleTimeString():"N/A"}})()),f(x,(()=>{var m=k(()=>!!E());return()=>m()?[(()=>{var S=Lt();return z(()=>s(S,t().detailsHeader)),S})(),(()=>{var S=xe();return f(S,G(le,{label:"loaderData",value:E,defaultExpanded:{}})),z(()=>s(S,t().detailsContent)),S})()]:null})(),ae),f(ue,G(le,{label:"Match",value:N,defaultExpanded:{}})),z(m=>{var S,Z,fe=t().thirdContainer,Ie=t().detailsHeader,Me=t().matchDetails,Ae=t().matchStatus((S=v())==null?void 0:S.status,(Z=v())==null?void 0:Z.isFetching),Te=t().matchDetailsInfoLabel,Pe=t().matchDetailsInfo,Le=t().matchDetailsInfoLabel,Re=t().matchDetailsInfo,je=t().matchDetailsInfoLabel,Oe=t().matchDetailsInfo,He=t().detailsHeader,Ge=t().detailsContent;return fe!==m.e&&s(x,m.e=fe),Ie!==m.t&&s(I,m.t=Ie),Me!==m.a&&s(w,m.a=Me),Ae!==m.o&&s(R,m.o=Ae),Te!==m.i&&s(D,m.i=Te),Pe!==m.n&&s(B,m.n=Pe),Le!==m.s&&s(q,m.s=Le),Re!==m.h&&s(Y,m.h=Re),je!==m.r&&s(re,m.r=je),Oe!==m.d&&s(ce,m.d=Oe),He!==m.l&&s(ae,m.l=He),Ge!==m.u&&s(ue,m.u=Ge),m},{e:void 0,t:void 0,a:void 0,o:void 0,i:void 0,n:void 0,s:void 0,h:void 0,r:void 0,d:void 0,l:void 0,u:void 0}),x})():null})(),null),f(_,(()=>{var c=k(()=>!!L());return()=>c()?(()=>{var x=Rt(),I=x.firstChild,M=I.nextSibling;return f(M,G(le,{value:K,get defaultExpanded(){return Object.keys(l().location.search).reduce((w,R)=>(w[R]={},w),{})}})),z(w=>{var R=t().fourthContainer,C=t().detailsHeader,D=t().detailsContent;return R!==w.e&&s(x,w.e=R),C!==w.t&&s(I,w.t=C),D!==w.a&&s(M,w.a=D),w},{e:void 0,t:void 0,a:void 0}),x})():null})(),null),z(c=>{var x=t().panelCloseBtn,I=t().panelCloseBtnIcon,M=t().firstContainer,w=t().row,R=t().routerExplorerContainer,C=t().routerExplorer,D=t().secondContainer,J=t().matchesContainer,B=t().detailsHeader,j=t().detailsContent,q=t().detailsHeader,W=t().routeMatchesToggle,Y=!T(),re=O(t().routeMatchesToggleBtn(!T(),!0)),me=T(),ce=O(t().routeMatchesToggleBtn(!!T(),!1)),ae=t().detailsHeaderInfo,ue=O(t().routesContainer);return x!==c.e&&s(V,c.e=x),I!==c.t&&ve(ge,"class",c.t=I),M!==c.a&&s(de,c.a=M),w!==c.o&&s(oe,c.o=w),R!==c.i&&s(H,c.i=R),C!==c.n&&s(U,c.n=C),D!==c.s&&s(te,c.s=D),J!==c.h&&s(Ee,c.h=J),B!==c.r&&s(he,c.r=B),j!==c.d&&s($e,c.d=j),q!==c.l&&s(we,c.l=q),W!==c.u&&s(Ce,c.u=W),Y!==c.c&&(be.disabled=c.c=Y),re!==c.w&&s(be,c.w=re),me!==c.m&&(ke.disabled=c.m=me),ce!==c.f&&s(ke,c.f=ce),ae!==c.y&&s(it,c.y=ae),ue!==c.g&&s(Be,c.g=ue),c},{e:void 0,t:void 0,a:void 0,o:void 0,i:void 0,n:void 0,s:void 0,h:void 0,r:void 0,d:void 0,l:void 0,u:void 0,c:void 0,w:void 0,m:void 0,f:void 0,y:void 0,g:void 0}),_})()};Qe(["click","mousedown"]);const Nt=Object.freeze(Object.defineProperty({__proto__:null,BaseTanStackRouterDevtoolsPanel:Ue,default:Ue},Symbol.toStringTag,{value:"Module"}));export{Ue as B,Gt as a,ye as b,Nt as c,Je as u};
