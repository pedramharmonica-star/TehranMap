import { useEffect, useRef } from 'react'
import type React from 'react'
import 'leaflet/dist/leaflet.css'
import './map.css'
import GEO from './geo.json'
import { initMap } from './mapEngine'

export default function App() {
  const done = useRef(false)
  useEffect(() => { if (done.current) return; done.current = true; initMap(GEO) }, [])
  return (<>

<div id="map" role="application" aria-label="نقشه محدوده پشتیبانی حضوری پیام‌گستر"></div>

<header className="brandcard glass">
  <div className="head">
    <div className="logo" id="logo" aria-label="پیام‌گستر"></div>
    <h1>محدوده پشتیبانی حضوری</h1>
  </div>
  <p>محله، شهر یا منطقه را جستجو کنید یا روی نقشه بزنید تا شرایط اعزام کارشناس را ببینید.</p>
  <div className="search">
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path className="a" d="M16 16l4.5 4.5"/></svg>
    <input id="q" type="search" placeholder="مثلاً سعادت‌آباد، قدس، منطقه ۵" autoComplete="off" aria-label="جستجوی محله، شهر یا منطقه" />
    <div className="results" id="results" hidden></div>
  </div>
</header>

<aside className="legend glass" id="legend" aria-label="راهنمای نقشه">
  <h2><span>راهنمای نقشه</span><button className="collapse" id="collapse" type="button">جمع کردن</button></h2>
  <button className="row" data-z="1" type="button" style={{"--rc":"var(--z1)"} as React.CSSProperties}><div className="sw sw1"></div><b>پشتیبانی حضوری</b><span>محدوده‌ی مناطق ۲۲گانه‌ی تهران</span></button>
  <button className="row" data-z="2" type="button" style={{"--rc":"var(--z2)"} as React.CSSProperties}><div className="sw sw2"></div><b>حضوری با هزینه ایاب و ذهاب</b><span>از مرز مناطق ۲۲گانه تا خط زرد</span></button>
  <button className="row" data-z="3" type="button" style={{"--rc":"var(--z3)"} as React.CSSProperties}><div className="sw sw3"></div><b>نیازمند تأیید فروشنده</b><span>بیرون از خط زرد، با هزینه‌ی ایاب و ذهاب و حق مأموریت</span></button>
  <div className="edgegrid">
    <div className="edge"><i></i>مرز ایاب و ذهاب</div>
    <div className="edge"><i className="g"></i>مرز مناطق تهران</div>
  </div>
</aside>

<div className="tag" id="tag" hidden></div>
<div className="loading" id="loading">در حال بارگذاری خیابان‌ها…</div>

  </>)
}
