import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
const STYLES = `
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Inter',sans-serif;background:#070710;color:#fff;overflow-x:hidden}
  ::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:#111}::-webkit-scrollbar-thumb{background:#e50914;border-radius:4px}
  input,textarea,select{font-family:'Inter',sans-serif}
  button{font-family:'Inter',sans-serif}

  @keyframes fadeUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
  @keyframes fadeIn{from{opacity:0}to{opacity:1}}
  @keyframes spin{to{transform:rotate(360deg)}}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.45}}
  @keyframes shimmer{0%{background-position:-400% 0}100%{background-position:400% 0}}
  @keyframes glow{0%,100%{box-shadow:0 0 18px rgba(229,9,20,.35)}50%{box-shadow:0 0 36px rgba(229,9,20,.75)}}
  @keyframes slideIn{from{opacity:0;transform:translateX(-16px)}to{opacity:1;transform:translateX(0)}}
  @keyframes modalIn{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:scale(1)}}
  @keyframes ratingCount{from{transform:scale(.7);opacity:0}to{transform:scale(1);opacity:1}}

  .fade-up{animation:fadeUp .55s ease both}
  .fade-in{animation:fadeIn .35s ease both}
  .pulse-dot{animation:pulse 1.4s ease infinite}
  .spin{animation:spin .9s linear infinite}
  .glow-btn{animation:glow 2.2s ease infinite}
  .slide-in{animation:slideIn .4s ease both}
  .modal-in{animation:modalIn .25s ease both}
  .rating-pop{animation:ratingCount .5s cubic-bezier(.34,1.56,.64,1) both}

  .shimmer{
    background:linear-gradient(90deg,#12122a 25%,#1a1a3a 50%,#12122a 75%);
    background-size:400% 100%;animation:shimmer 1.6s infinite;
  }
  .glass{background:rgba(255,255,255,.04);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.07)}
  .card-lift{transition:transform .28s ease,box-shadow .28s ease;cursor:pointer}
  .card-lift:hover{transform:translateY(-7px) scale(1.02);box-shadow:0 18px 56px rgba(229,9,20,.28)}
  .grad-text{background:linear-gradient(135deg,#e50914,#ff6b35);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
  .input-focus:focus{outline:none;box-shadow:0 0 0 2px rgba(229,9,20,.5),0 0 28px rgba(229,9,20,.15)}
  .chip-hover{transition:all .18s;cursor:pointer}
  .chip-hover:hover{background:rgba(229,9,20,.18);border-color:#e50914;transform:scale(1.04)}
  .tab-active{background:#e50914;color:#fff}
  .tab-inactive{background:transparent;color:rgba(255,255,255,.45)}
  .tab-inactive:hover{color:#fff;background:rgba(255,255,255,.07)}
  .overlay{position:fixed;inset:0;background:rgba(0,0,0,.75);backdrop-filter:blur(6px);z-index:1000;display:flex;align-items:center;justify-content:center;padding:1rem}
  .modal{background:#0f0f1e;border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:2rem;width:100%;max-width:520px;max-height:90vh;overflow-y:auto;position:relative}
  .form-input{width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);color:#fff;padding:10px 14px;border-radius:10px;font-size:.9rem;transition:border-color .2s}
  .form-input:focus{outline:none;border-color:#e50914;background:rgba(255,255,255,.07)}
  .form-input::placeholder{color:rgba(255,255,255,.3)}
  .form-label{font-size:.78rem;font-weight:600;color:rgba(255,255,255,.55);margin-bottom:5px;display:block;text-transform:uppercase;letter-spacing:.5px}
  .badge-tmdb{background:rgba(1,180,228,.12);border:1px solid rgba(1,180,228,.3);color:#01b4e4}
  .badge-user{background:rgba(255,165,0,.12);border:1px solid rgba(255,165,0,.3);color:#ffa500}
  .badge-ai{background:rgba(168,85,247,.12);border:1px solid rgba(168,85,247,.3);color:#c084fc}
  .source-dot-tmdb{background:#01b4e4}
  .source-dot-user{background:#ffa500}
  .nav-link{color:rgba(255,255,255,.6);font-size:.88rem;cursor:pointer;transition:color .2s;text-decoration:none}
  .nav-link:hover{color:#fff}
  @media(max-width:768px){
    .hero-h1{font-size:2rem!important}
    .grid-movies{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))!important}
    .action-btns{flex-direction:column!important;gap:8px!important}
    .hero-stats{gap:1.5rem!important}
    .modal{padding:1.25rem}
    .nav-links{display:none}
  }
  @media(max-width:480px){.grid-movies{grid-template-columns:repeat(2,1fr)!important}}
`;

// ─── ICONS ────────────────────────────────────────────────────────────────────
const I = {
  Search: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>,
  Star: ({f,s=14}) => <svg width={s} height={s} viewBox="0 0 24 24" fill={f?"#FFD700":"none"} stroke="#FFD700" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>,
  Plus: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>,
  Wand: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 4-1 1"/><path d="m4 15 1-1"/><path d="m12 2 .5 1.5L14 4l-1.5.5L12 6l-.5-1.5L10 4l1.5-.5Z"/><path d="m18 12 .5 1.5 1.5.5-1.5.5L18 16l-.5-1.5L16 14l1.5-.5Z"/><path d="M3 3l9 9"/><path d="m13 3 8 8"/><path d="m3 13 8 8"/></svg>,
  Brain: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.46 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.14Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.46 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.14Z"/></svg>,
  Sparkle: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>,
  X: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>,
  Film: ({s=20}) => <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="2" width="20" height="20" rx="2"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="17" y1="7" x2="22" y2="7"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="2" y1="17" x2="7" y2="17"/></svg>,
  Check: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>,
  Down: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="6 9 12 15 18 9"/></svg>,
  Link: () => <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>,
  Grid: () => <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>,
  Save: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>,
  Clapperboard: () => <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 3.9"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/></svg>,
};

// ─── UTILITIES ────────────────────────────────────────────────────────────────
const Spinner = ({s=16,c='#fff'}) => (
  <span className="spin" style={{display:'inline-block',width:s,height:s,border:`2px solid rgba(255,255,255,.2)`,borderTopColor:c,borderRadius:'50%'}}/>
);

const StarRow = ({rating=0,max=5,size=13}) => {
  const filled = Math.round((rating/10)*max);
  return (
    <span style={{display:'flex',gap:2,alignItems:'center'}}>
      {Array.from({length:max},(_,i)=><I.Star key={i} f={i<filled} s={size}/>)}
    </span>
  );
};

const GenreBadge = ({label}) => (
  <span style={{background:'rgba(229,9,20,.13)',border:'1px solid rgba(229,9,20,.28)',color:'#ff7070',padding:'2px 9px',borderRadius:20,fontSize:'.65rem',fontWeight:600}}>{label}</span>
);

const SourceBadge = ({source}) => {
  const cfg = source==='user'
    ? {cls:'badge-user',label:'👤 My Movie'}
    : source==='tmdb'
    ? {cls:'badge-tmdb',label:'🎬 TMDB'}
    : {cls:'badge-ai',label:'🤖 AI Rated'};
  return <span className={cfg.cls} style={{padding:'2px 9px',borderRadius:20,fontSize:'.62rem',fontWeight:700}}>{cfg.label}</span>;
};

function Toast({msg,type='success',onClose}) {
  useEffect(()=>{const t=setTimeout(onClose,3500);return()=>clearTimeout(t)},[onClose]);
  const bg = type==='error'?'#c0392b':type==='info'?'#2980b9':'#27ae60';
  return (
    <div style={{position:'fixed',top:80,right:20,zIndex:3000,background:bg,color:'#fff',padding:'12px 20px',borderRadius:12,
      maxWidth:320,boxShadow:'0 8px 32px rgba(0,0,0,.4)',display:'flex',alignItems:'center',gap:10,animation:'fadeUp .3s ease'}}>
      <span style={{flex:1,fontSize:'.88rem',fontWeight:500}}>{msg}</span>
      <button onClick={onClose} style={{background:'none',border:'none',color:'rgba(255,255,255,.7)',cursor:'pointer',padding:2}}><I.X/></button>
    </div>
  );
}

// ─── MOVIE CARD ───────────────────────────────────────────────────────────────
function MovieCard({movie,index=0,showSource=false}) {
  const [imgErr,setImgErr] = useState(false);
  const [exp,setExp]       = useState(false);
  const src   = movie.source || 'tmdb';
  const rating = movie.ai_rating || movie.rating || 0;
  const delay  = `${Math.min(index*0.06,0.5)}s`;

  return (
    <div className="card-lift glass fade-in" style={{borderRadius:14,overflow:'hidden',animationDelay:delay,display:'flex',flexDirection:'column'}}>
      {/* Poster */}
      <div style={{position:'relative',aspectRatio:'2/3',overflow:'hidden',flexShrink:0,background:'linear-gradient(135deg,#12122a,#1e1e40)'}}>
        {movie.poster && !imgErr
          ? <img src={movie.poster} alt={movie.title} onError={()=>setImgErr(true)}
              style={{width:'100%',height:'100%',objectFit:'cover',transition:'transform .4s ease'}}
              onMouseEnter={e=>e.currentTarget.style.transform='scale(1.07)'}
              onMouseLeave={e=>e.currentTarget.style.transform='scale(1)'}/>
          : <div style={{width:'100%',height:'100%',display:'flex',alignItems:'center',justifyContent:'center',opacity:.3}}>
              <I.Film s={36}/>
            </div>
        }
        {/* badges overlay */}
        <div style={{position:'absolute',top:8,right:8,display:'flex',flexDirection:'column',gap:4,alignItems:'flex-end'}}>
          <span style={{background:'rgba(0,0,0,.82)',backdropFilter:'blur(6px)',padding:'3px 9px',borderRadius:20,fontSize:'.72rem',fontWeight:700,display:'flex',alignItems:'center',gap:3}}>
            <I.Star f s={11}/> {rating.toFixed(1)}
          </span>
          {showSource && <SourceBadge source={src}/>}
        </div>
        {movie.year && <span style={{position:'absolute',top:8,left:8,background:'#e50914',padding:'2px 8px',borderRadius:20,fontSize:'.62rem',fontWeight:700}}>{movie.year}</span>}
        <div style={{position:'absolute',bottom:0,left:0,right:0,height:'55%',background:'linear-gradient(transparent,rgba(7,7,16,.97)',pointerEvents:'none'}}/>
      </div>
      {/* Info */}
      <div style={{padding:'12px 14px 14px',display:'flex',flexDirection:'column',gap:6,flex:1}}>
        <div style={{fontWeight:700,fontSize:'.9rem',lineHeight:1.25}}>{movie.title}</div>
        <StarRow rating={rating}/>
        <div style={{display:'flex',flexWrap:'wrap',gap:4}}>
          {(movie.genres||[]).slice(0,2).map(g=><GenreBadge key={g} label={g}/>)}
          {movie.certification && <span style={{background:'rgba(255,255,255,.06)',border:'1px solid rgba(255,255,255,.12)',color:'rgba(255,255,255,.6)',padding:'2px 7px',borderRadius:20,fontSize:'.62rem',fontWeight:600}}>{movie.certification}</span>}
        </div>
        {movie.ai_review && (
          <div style={{background:'rgba(168,85,247,.08)',border:'1px solid rgba(168,85,247,.2)',borderRadius:8,padding:'6px 9px',fontSize:'.71rem',color:'#c084fc',lineHeight:1.5}}>
            🤖 {movie.ai_review.slice(0,100)}{movie.ai_review.length>100?'…':''}
          </div>
        )}
        <p style={{fontSize:'.73rem',color:'rgba(255,255,255,.45)',lineHeight:1.5,display:'-webkit-box',WebkitLineClamp:exp?99:3,WebkitBoxOrient:'vertical',overflow:'hidden'}}>
          {movie.overview||'No overview available.'}
        </p>
        {(movie.overview||'').length>120 && (
          <button onClick={()=>setExp(!exp)} style={{background:'none',border:'none',color:'#e50914',fontSize:'.7rem',cursor:'pointer',padding:0,textAlign:'left'}}>
            {exp?'Less ↑':'More ↓'}
          </button>
        )}
        {movie.tmdb_url && (
          <a href={movie.tmdb_url} target="_blank" rel="noopener noreferrer"
            style={{fontSize:'.68rem',color:'rgba(255,255,255,.25)',textDecoration:'none',display:'flex',alignItems:'center',gap:3,marginTop:2,transition:'color .18s'}}
            onMouseEnter={e=>e.currentTarget.style.color='#e50914'}
            onMouseLeave={e=>e.currentTarget.style.color='rgba(255,255,255,.25)'}>
            <I.Link/> TMDB
          </a>
        )}
      </div>
    </div>
  );
}

// ─── ADD MOVIE MODAL ──────────────────────────────────────────────────────────
const GENRES_LIST = ['Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','Horror','Music','Mystery','Romance','Science Fiction','Thriller','War','Western'];
const CERTS_LIST  = ['G','PG','PG-13','R','NC-17','NR'];

function AddMovieModal({onClose,onSaved}) {
  const [form,setForm] = useState({title:'',year:'',rating:'',overview:'',genres:[],certification:'',language:'en',poster:'',director:''});
  const [loading,setLoading] = useState(false);
  const [err,setErr]   = useState('');

  const toggleGenre = g => setForm(f=>({...f,genres:f.genres.includes(g)?f.genres.filter(x=>x!==g):[...f.genres,g]}));
  const set = k => e => setForm(f=>({...f,[k]:e.target.value}));

  const submit = async() => {
    if(!form.title.trim()){setErr('Movie title is required.');return;}
    if(form.year && !/^\d{4}$/.test(form.year)){setErr('Year must be 4 digits.');return;}
    if(form.rating && (isNaN(form.rating)||+form.rating<0||+form.rating>10)){setErr('Rating must be 0–10.');return;}
    setLoading(true); setErr('');
    try {
      const payload = {...form, rating: form.rating?+form.rating:undefined};
      await axios.post(`${API}/movies/add`, payload);
      onSaved(`"${form.title}" added to your collection!`);
      onClose();
    } catch(e) {
      setErr(e.response?.data?.detail || 'Failed to add movie.');
    } finally { setLoading(false); }
  };

  return (
    <div className="overlay" onClick={e=>e.target===e.currentTarget&&onClose()}>
      <div className="modal modal-in">
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'1.5rem'}}>
          <div>
            <h2 style={{fontSize:'1.3rem',fontWeight:800}}>+ Add My Movie</h2>
            <p style={{color:'rgba(255,255,255,.4)',fontSize:'.8rem',marginTop:3}}>Permanently saved — searchable by the AI agent</p>
          </div>
          <button onClick={onClose} style={{background:'rgba(255,255,255,.07)',border:'none',color:'rgba(255,255,255,.6)',width:32,height:32,borderRadius:'50%',cursor:'pointer',display:'flex',alignItems:'center',justifyContent:'center'}}><I.X/></button>
        </div>

        <div style={{display:'flex',flexDirection:'column',gap:'1rem'}}>
          {/* Title */}
          <div>
            <label className="form-label">Movie Title *</label>
            <input className="form-input input-focus" value={form.title} onChange={set('title')} placeholder="e.g. The Dark Knight"/>
          </div>
          {/* Year + Rating row */}
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1rem'}}>
            <div>
              <label className="form-label">Release Year</label>
              <input className="form-input input-focus" value={form.year} onChange={set('year')} placeholder="e.g. 2008" maxLength={4}/>
            </div>
            <div>
              <label className="form-label">Rating (0–10)</label>
              <input className="form-input input-focus" type="number" min="0" max="10" step="0.1" value={form.rating} onChange={set('rating')} placeholder="e.g. 9.0"/>
            </div>
          </div>
          {/* Genres */}
          <div>
            <label className="form-label">Genres (select all that apply)</label>
            <div style={{display:'flex',flexWrap:'wrap',gap:6,marginTop:4}}>
              {GENRES_LIST.map(g=>(
                <button key={g} onClick={()=>toggleGenre(g)}
                  style={{padding:'4px 12px',borderRadius:20,border:'1px solid',fontSize:'.72rem',fontWeight:600,cursor:'pointer',transition:'all .18s',
                    background:form.genres.includes(g)?'rgba(229,9,20,.2)':'rgba(255,255,255,.04)',
                    borderColor:form.genres.includes(g)?'#e50914':'rgba(255,255,255,.12)',
                    color:form.genres.includes(g)?'#ff7070':'rgba(255,255,255,.5)'}}>
                  {form.genres.includes(g)?'✓ ':''}{g}
                </button>
              ))}
            </div>
          </div>
          {/* Cert + Lang row */}
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1rem'}}>
            <div>
              <label className="form-label">Age Rating</label>
              <select className="form-input input-focus" value={form.certification} onChange={set('certification')}
                style={{appearance:'none',background:'rgba(255,255,255,.05)',color:form.certification?'#fff':'rgba(255,255,255,.3)'}}>
                <option value="">Select…</option>
                {CERTS_LIST.map(c=><option key={c} value={c} style={{background:'#12122a'}}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="form-label">Language</label>
              <select className="form-input input-focus" value={form.language} onChange={set('language')}
                style={{appearance:'none',background:'rgba(255,255,255,.05)',color:'#fff'}}>
                {[['en','English'],['hi','Hindi'],['ja','Japanese'],['ko','Korean'],['fr','French'],['es','Spanish'],['de','German'],['ta','Tamil']].map(([c,l])=>
                  <option key={c} value={c} style={{background:'#12122a'}}>{l}</option>)}
              </select>
            </div>
          </div>
          {/* Overview */}
          <div>
            <label className="form-label">Overview / Description</label>
            <textarea className="form-input input-focus" value={form.overview} onChange={set('overview')}
              placeholder="A brief description of the movie…" rows={3} style={{resize:'vertical'}}/>
          </div>
          {/* Director + Poster row */}
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1rem'}}>
            <div>
              <label className="form-label">Director</label>
              <input className="form-input input-focus" value={form.director} onChange={set('director')} placeholder="e.g. Christopher Nolan"/>
            </div>
            <div>
              <label className="form-label">Poster URL (optional)</label>
              <input className="form-input input-focus" value={form.poster} onChange={set('poster')} placeholder="https://…"/>
            </div>
          </div>

          {err && <div style={{background:'rgba(229,9,20,.1)',border:'1px solid rgba(229,9,20,.3)',borderRadius:8,padding:'8px 12px',color:'#ff7070',fontSize:'.8rem'}}>{err}</div>}

          <button onClick={submit} disabled={loading} style={{background:'linear-gradient(135deg,#e50914,#ff4444)',color:'#fff',border:'none',padding:'12px',borderRadius:11,fontWeight:700,fontSize:'.95rem',cursor:loading?'not-allowed':'pointer',opacity:loading?.7:1,display:'flex',alignItems:'center',justifyContent:'center',gap:8}}>
            {loading?<><Spinner/> Saving…</>:<><I.Save/> Save to My Movies</>}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── RATE MOVIE MODAL ─────────────────────────────────────────────────────────
function RateMovieModal({onClose,onSaved}) {
  const [form,setForm] = useState({title:'',year:'',genres:[],overview:''});
  const [result,setResult]   = useState(null);
  const [loading,setLoading] = useState(false);
  const [saving,setSaving]   = useState(false);
  const [err,setErr]         = useState('');

  const toggleGenre = g => setForm(f=>({...f,genres:f.genres.includes(g)?f.genres.filter(x=>x!==g):[...f.genres,g]}));
  const set = k => e => setForm(f=>({...f,[k]:e.target.value}));

  const analyze = async() => {
    if(!form.title.trim()){setErr('Movie title is required.');return;}
    setLoading(true); setErr(''); setResult(null);
    try {
      const {data} = await axios.post(`${API}/movies/rate`,{title:form.title.trim(),year:form.year||null,genres:form.genres,overview:form.overview||null});
      setResult(data);
    } catch(e) {
      setErr(e.response?.data?.detail||'Failed to rate movie. Try again.');
    } finally { setLoading(false); }
  };

  const saveToCollection = async() => {
    if(!result) return;
    setSaving(true);
    try {
      await axios.post(`${API}/movies/save-rating`,{
        title:result.title, year:result.year, overview:result.overview,
        genres:form.genres, ai_rating:result.ai_rating,
        ai_review:result.ai_review, ai_reasoning:result.ai_reasoning,
        suitability:result.suitability, poster:result.poster||null,
      });
      onSaved(`"${result.title}" rated & saved to your collection!`);
      onClose();
    } catch(e) {
      setErr(e.response?.data?.detail||'Save failed.');
    } finally { setSaving(false); }
  };

  const ratingColor = r => r>=8?'#22c55e':r>=6?'#eab308':'#ef4444';

  return (
    <div className="overlay" onClick={e=>e.target===e.currentTarget&&onClose()}>
      <div className="modal modal-in" style={{maxWidth:560}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'1.4rem'}}>
          <div>
            <h2 style={{fontSize:'1.3rem',fontWeight:800}}>🤖 Rate My Movie</h2>
            <p style={{color:'rgba(255,255,255,.4)',fontSize:'.8rem',marginTop:3}}>AI analyzes & generates a rating with full reasoning</p>
          </div>
          <button onClick={onClose} style={{background:'rgba(255,255,255,.07)',border:'none',color:'rgba(255,255,255,.6)',width:32,height:32,borderRadius:'50%',cursor:'pointer',display:'flex',alignItems:'center',justifyContent:'center'}}><I.X/></button>
        </div>

        {!result ? (
          <div style={{display:'flex',flexDirection:'column',gap:'1rem'}}>
            <div>
              <label className="form-label">Movie Title *</label>
              <input className="form-input input-focus" value={form.title} onChange={set('title')} placeholder="e.g. Hereditary"/>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1rem'}}>
              <div>
                <label className="form-label">Release Year</label>
                <input className="form-input input-focus" value={form.year} onChange={set('year')} placeholder="e.g. 2018" maxLength={4}/>
              </div>
              <div>
                <label className="form-label">Overview (optional)</label>
                <input className="form-input input-focus" value={form.overview} onChange={set('overview')} placeholder="Brief description…"/>
              </div>
            </div>
            <div>
              <label className="form-label">Genres (optional — helps AI)</label>
              <div style={{display:'flex',flexWrap:'wrap',gap:6,marginTop:4}}>
                {['Horror','Thriller','Drama','Comedy','Action','Sci-Fi','Mystery','Romance'].map(g=>(
                  <button key={g} onClick={()=>toggleGenre(g)}
                    style={{padding:'4px 12px',borderRadius:20,border:'1px solid',fontSize:'.72rem',cursor:'pointer',transition:'all .18s',
                      background:form.genres.includes(g)?'rgba(168,85,247,.2)':'rgba(255,255,255,.04)',
                      borderColor:form.genres.includes(g)?'#a855f7':'rgba(255,255,255,.12)',
                      color:form.genres.includes(g)?'#c084fc':'rgba(255,255,255,.5)'}}>
                    {form.genres.includes(g)?'✓ ':''}{g}
                  </button>
                ))}
              </div>
            </div>
            {err && <div style={{background:'rgba(229,9,20,.1)',border:'1px solid rgba(229,9,20,.3)',borderRadius:8,padding:'8px 12px',color:'#ff7070',fontSize:'.8rem'}}>{err}</div>}
            <button onClick={analyze} disabled={loading}
              style={{background:'linear-gradient(135deg,#7c3aed,#a855f7)',color:'#fff',border:'none',padding:'12px',borderRadius:11,fontWeight:700,cursor:loading?'not-allowed':'pointer',display:'flex',alignItems:'center',justifyContent:'center',gap:8}}>
              {loading?<><Spinner/> AI is analyzing…</>:<><I.Wand/> Analyze & Rate</>}
            </button>
          </div>
        ) : (
          <div style={{display:'flex',flexDirection:'column',gap:'1.2rem'}} className="fade-in">
            {/* Poster + Rating hero */}
            <div style={{display:'flex',gap:'1.2rem',alignItems:'flex-start'}}>
              {result.poster && (
                <img src={result.poster} alt={result.title}
                  style={{width:90,height:130,objectFit:'cover',borderRadius:10,flexShrink:0,border:'2px solid rgba(255,255,255,.08)'}}
                  onError={e=>{e.currentTarget.style.display='none'}}/>
              )}
              <div style={{flex:1}}>
                <div style={{fontSize:'1.1rem',fontWeight:800,lineHeight:1.2,marginBottom:4}}>{result.title}{result.year?` (${result.year})`:''}</div>
                {result.tmdb_rating && <div style={{color:'rgba(255,255,255,.4)',fontSize:'.75rem',marginBottom:8}}>TMDB Community: {result.tmdb_rating}/10</div>}
                {/* Big AI rating */}
                <div className="rating-pop" style={{display:'inline-flex',alignItems:'center',gap:10,background:'rgba(0,0,0,.3)',border:'1px solid rgba(255,255,255,.1)',borderRadius:12,padding:'10px 16px'}}>
                  <div style={{fontSize:'2.4rem',fontWeight:900,color:ratingColor(result.ai_rating),lineHeight:1}}>{result.ai_rating.toFixed(1)}</div>
                  <div>
                    <div style={{fontSize:'.65rem',color:'rgba(255,255,255,.4)',textTransform:'uppercase',letterSpacing:'.5px'}}>AI Rating</div>
                    <StarRow rating={result.ai_rating} size={14}/>
                  </div>
                </div>
              </div>
            </div>

            {/* Genre tags */}
            {result.genre_tags?.length>0 && (
              <div style={{display:'flex',flexWrap:'wrap',gap:6}}>
                {result.genre_tags.map(t=><span key={t} className="badge-ai" style={{padding:'3px 10px',borderRadius:20,fontSize:'.7rem',fontWeight:600}}>{t}</span>)}
              </div>
            )}

            {/* Review */}
            <div style={{background:'rgba(168,85,247,.08)',border:'1px solid rgba(168,85,247,.2)',borderRadius:10,padding:'12px 14px'}}>
              <div style={{color:'#c084fc',fontWeight:700,fontSize:'.75rem',marginBottom:6,textTransform:'uppercase',letterSpacing:'.5px'}}>🤖 AI Review</div>
              <p style={{color:'rgba(255,255,255,.8)',fontSize:'.85rem',lineHeight:1.65}}>{result.ai_review}</p>
            </div>

            {/* Reasoning */}
            <div style={{background:'rgba(99,102,241,.08)',border:'1px solid rgba(99,102,241,.2)',borderRadius:10,padding:'12px 14px'}}>
              <div style={{color:'#a5b4fc',fontWeight:700,fontSize:'.75rem',marginBottom:6,textTransform:'uppercase',letterSpacing:'.5px'}}>🧠 Reasoning</div>
              <p style={{color:'rgba(255,255,255,.65)',fontSize:'.82rem',lineHeight:1.6}}>{result.ai_reasoning}</p>
            </div>

            {/* Suitability */}
            {result.suitability && (
              <div style={{background:'rgba(16,185,129,.07)',border:'1px solid rgba(16,185,129,.2)',borderRadius:10,padding:'10px 14px'}}>
                <div style={{color:'#6ee7b7',fontWeight:700,fontSize:'.73rem',marginBottom:4,textTransform:'uppercase',letterSpacing:'.5px'}}>👥 Who Should Watch</div>
                <p style={{color:'rgba(255,255,255,.65)',fontSize:'.82rem'}}>{result.suitability}</p>
              </div>
            )}

            {err && <div style={{background:'rgba(229,9,20,.1)',border:'1px solid rgba(229,9,20,.3)',borderRadius:8,padding:'8px 12px',color:'#ff7070',fontSize:'.8rem'}}>{err}</div>}

            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'0.75rem'}}>
              <button onClick={()=>setResult(null)} style={{background:'rgba(255,255,255,.06)',border:'1px solid rgba(255,255,255,.12)',color:'rgba(255,255,255,.7)',padding:'10px',borderRadius:10,fontWeight:600,cursor:'pointer',fontSize:'.85rem'}}>
                ← Rate Another
              </button>
              <button onClick={saveToCollection} disabled={saving}
                style={{background:'linear-gradient(135deg,#e50914,#ff4444)',color:'#fff',border:'none',padding:'10px',borderRadius:10,fontWeight:700,cursor:saving?'not-allowed':'pointer',display:'flex',alignItems:'center',justifyContent:'center',gap:6,fontSize:'.85rem'}}>
                {saving?<><Spinner/> Saving…</>:<><I.Save/> Save to My Movies</>}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── NAVBAR ───────────────────────────────────────────────────────────────────
function Navbar({onAddMovie,onRateMovie,onScrollSearch,dbCount}) {
  const [scrolled,setScrolled] = useState(false);
  useEffect(()=>{const h=()=>setScrolled(window.scrollY>40);window.addEventListener('scroll',h);return()=>window.removeEventListener('scroll',h)},[]);
  return (
    <nav style={{position:'fixed',top:0,left:0,right:0,zIndex:900,padding:'0 1.5rem',height:64,display:'flex',alignItems:'center',justifyContent:'space-between',
      background:scrolled?'rgba(7,7,16,.96)':'transparent',
      backdropFilter:scrolled?'blur(18px)':'none',
      borderBottom:scrolled?'1px solid rgba(255,255,255,.06)':'none',
      transition:'all .3s ease'}}>
      <div style={{display:'flex',alignItems:'center',gap:9}}>
        <div style={{color:'#e50914'}}><I.Clapperboard/></div>
        <span style={{fontSize:'1.35rem',fontWeight:900,letterSpacing:'-0.5px'}}>Cine<span style={{color:'#e50914'}}>AI</span></span>
        {dbCount>0 && <span style={{background:'rgba(1,180,228,.12)',border:'1px solid rgba(1,180,228,.2)',color:'#01b4e4',padding:'2px 9px',borderRadius:20,fontSize:'.65rem',fontWeight:700,marginLeft:4}}>{dbCount}+ movies</span>}
      </div>
      <div className="nav-links" style={{display:'flex',gap:'1.5rem',alignItems:'center'}}>
        <span className="nav-link" onClick={onScrollSearch}>Discover</span>
        <button onClick={onAddMovie} style={{background:'rgba(255,165,0,.1)',border:'1px solid rgba(255,165,0,.3)',color:'#ffa500',padding:'6px 14px',borderRadius:8,fontWeight:700,fontSize:'.8rem',cursor:'pointer',display:'flex',alignItems:'center',gap:5,transition:'all .2s'}}
          onMouseEnter={e=>{e.currentTarget.style.background='rgba(255,165,0,.2)';}}
          onMouseLeave={e=>{e.currentTarget.style.background='rgba(255,165,0,.1)';}}><I.Plus/> Add My Movie</button>
        <button onClick={onRateMovie} style={{background:'rgba(168,85,247,.1)',border:'1px solid rgba(168,85,247,.3)',color:'#c084fc',padding:'6px 14px',borderRadius:8,fontWeight:700,fontSize:'.8rem',cursor:'pointer',display:'flex',alignItems:'center',gap:5,transition:'all .2s'}}
          onMouseEnter={e=>{e.currentTarget.style.background='rgba(168,85,247,.2)';}}
          onMouseLeave={e=>{e.currentTarget.style.background='rgba(168,85,247,.1)';}}><I.Wand/> Rate My Movie</button>
        <button onClick={onScrollSearch} style={{background:'linear-gradient(135deg,#e50914,#ff4444)',color:'#fff',border:'none',padding:'8px 18px',borderRadius:50,fontWeight:700,fontSize:'.82rem',cursor:'pointer'}}>
          Get Recs
        </button>
      </div>
    </nav>
  );
}

// ─── HERO ─────────────────────────────────────────────────────────────────────
function Hero({trending,onScroll,onAddMovie,onRateMovie,dbCount}) {
  const bg = trending[0]?.backdrop;
  return (
    <section style={{minHeight:'100vh',position:'relative',display:'flex',alignItems:'center',overflow:'hidden'}}>
      {bg && <div style={{position:'absolute',inset:0,backgroundImage:`url(${bg})`,backgroundSize:'cover',backgroundPosition:'center',opacity:.12}}/>}
      <div style={{position:'absolute',inset:0,background:'linear-gradient(to bottom,rgba(7,7,16,.5) 0%,rgba(7,7,16,.85) 60%,#070710 100%)'}}/>
      <div style={{position:'absolute',top:'15%',left:'-8%',width:480,height:480,background:'radial-gradient(circle,rgba(229,9,20,.12) 0%,transparent 70%)',pointerEvents:'none'}}/>
      <div style={{position:'absolute',bottom:'15%',right:'-8%',width:380,height:380,background:'radial-gradient(circle,rgba(168,85,247,.08) 0%,transparent 70%)',pointerEvents:'none'}}/>

      <div style={{position:'relative',zIndex:1,maxWidth:920,margin:'0 auto',padding:'0 1.5rem',textAlign:'center',paddingTop:80}}>
        <div className="fade-up" style={{marginBottom:'1.2rem'}}>
          <span style={{display:'inline-flex',alignItems:'center',gap:6,background:'rgba(229,9,20,.12)',border:'1px solid rgba(229,9,20,.28)',color:'#ff7070',padding:'5px 15px',borderRadius:50,fontSize:'.72rem',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase'}}>
            <I.Sparkle/> ReAct AI · Live TMDB · {dbCount>0?`${dbCount}+ Movies`:'Persistent DB'}
          </span>
        </div>
        <h1 className="fade-up hero-h1" style={{fontSize:'3.6rem',fontWeight:900,lineHeight:1.08,letterSpacing:'-1.5px',marginBottom:'1rem',animationDelay:'.1s'}}>
          Your Personal<br/><span className="grad-text">AI Movie Agent</span>
        </h1>
        <p className="fade-up" style={{fontSize:'1.1rem',color:'rgba(255,255,255,.55)',lineHeight:1.7,maxWidth:580,margin:'0 auto 2rem',animationDelay:'.2s'}}>
          Ask in plain English. Get real TMDB recommendations, add your own movies, and let AI rate any film — all persistent.
        </p>

        <div className="fade-up action-btns" style={{display:'flex',gap:'0.75rem',justifyContent:'center',flexWrap:'wrap',animationDelay:'.3s'}}>
          <button onClick={onScroll} className="glow-btn" style={{background:'linear-gradient(135deg,#e50914,#ff4444)',color:'#fff',border:'none',padding:'14px 32px',borderRadius:50,fontSize:'1rem',fontWeight:800,cursor:'pointer',display:'flex',alignItems:'center',gap:7}}>
            <I.Sparkle/> Discover Movies
          </button>
          <button onClick={onAddMovie} style={{background:'rgba(255,165,0,.1)',border:'1px solid rgba(255,165,0,.35)',color:'#ffa500',padding:'14px 28px',borderRadius:50,fontSize:'.95rem',fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:6,transition:'all .2s'}}
            onMouseEnter={e=>e.currentTarget.style.background='rgba(255,165,0,.2)'}
            onMouseLeave={e=>e.currentTarget.style.background='rgba(255,165,0,.1)'}><I.Plus/> Add My Movie</button>
          <button onClick={onRateMovie} style={{background:'rgba(168,85,247,.1)',border:'1px solid rgba(168,85,247,.35)',color:'#c084fc',padding:'14px 28px',borderRadius:50,fontSize:'.95rem',fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:6,transition:'all .2s'}}
            onMouseEnter={e=>e.currentTarget.style.background='rgba(168,85,247,.2)'}
            onMouseLeave={e=>e.currentTarget.style.background='rgba(168,85,247,.1)'}><I.Wand/> Rate My Movie</button>
        </div>

        <div className="fade-up hero-stats" style={{display:'flex',gap:'3rem',justifyContent:'center',marginTop:'3.5rem',animationDelay:'.4s'}}>
          {[[dbCount>0?`${dbCount}+`:'150+','Movies in DB'],['ReAct','Architecture'],['Live','TMDB Data'],['SQLite','Persistent']].map(([n,l])=>(
            <div key={l} style={{textAlign:'center'}}>
              <div style={{fontSize:'1.6rem',fontWeight:900,color:'#e50914'}}>{n}</div>
              <div style={{fontSize:'.72rem',color:'rgba(255,255,255,.35)',marginTop:3}}>{l}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ─── SEARCH SECTION ───────────────────────────────────────────────────────────
const SUGGESTIONS = [
  'Horror movie from the 90s rated R',
  'Top 3 sci-fi from 2010s above 8 rating',
  'Japanese animated movie',
  'Hindi comedy above 8 rating',
  'Korean thriller 2019',
  'PG-13 family adventure',
  'Classic drama above 9 rating',
  'Action movie from the 80s',
  'French comedy drama',
  'Crime movie above 8.5',
];

function SearchSection({searchRef,onSearch,loading}) {
  const [query,setQuery]   = useState('');
  const [mode,setMode]     = useState('direct');

  const fire = useCallback(q=>{
    const fq=(q||query).trim();
    if(!fq) return;
    if(q) setQuery(q);
    onSearch(fq, mode==='agent');
  },[query,mode,onSearch]);

  return (
    <section ref={searchRef} style={{padding:'5rem 1.5rem 3rem',background:'linear-gradient(180deg,#070710 0%,#0b0b1a 100%)'}}>
      <div style={{textAlign:'center',marginBottom:'2rem'}}>
        <h2 style={{fontSize:'2rem',fontWeight:900,marginBottom:6}}>Ask the <span className="grad-text">AI Agent</span></h2>
        <p style={{color:'rgba(255,255,255,.4)',fontSize:'.9rem'}}>Natural language → Constraint extraction → TMDB Live + Local DB + Your Movies</p>
      </div>

      {/* Mode toggle */}
      <div style={{display:'flex',justifyContent:'center',alignItems:'center',gap:12,marginBottom:'1.25rem',flexWrap:'wrap'}}>
        <div style={{display:'flex',background:'rgba(255,255,255,.04)',border:'1px solid rgba(255,255,255,.09)',borderRadius:50,padding:3}}>
          {[['direct','⚡ TMDB Direct','Fast — no OpenAI cost'],['agent','🧠 ReAct Agent','Full LangChain reasoning (needs OpenAI key)']].map(([v,l,t])=>(
            <button key={v} onClick={()=>setMode(v)} title={t}
              style={{padding:'7px 18px',borderRadius:50,border:'none',background:mode===v?'#e50914':'transparent',
                color:mode===v?'#fff':'rgba(255,255,255,.45)',fontSize:'.82rem',fontWeight:mode===v?700:400,cursor:'pointer',transition:'all .2s'}}>
              {l}
            </button>
          ))}
        </div>
        <span style={{fontSize:'.72rem',color:'rgba(255,255,255,.28)'}}>{mode==='agent'?'Requires OPENAI_API_KEY':'Only TMDB key needed'}</span>
      </div>

      {/* Input */}
      <div style={{maxWidth:760,margin:'0 auto'}}>
        <div style={{display:'flex',gap:10,alignItems:'center',background:'rgba(255,255,255,.05)',border:'1px solid rgba(255,255,255,.1)',borderRadius:14,padding:'7px 7px 7px 18px',boxShadow:'0 6px 36px rgba(0,0,0,.4)'}}>
          <span style={{color:'rgba(255,255,255,.28)',flexShrink:0}}><I.Search/></span>
          <input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&fire()}
            placeholder='"Recommend a horror movie from the 90s rated R…"'
            className="input-focus" style={{flex:1,background:'transparent',border:'none',color:'#fff',fontSize:'.95rem',padding:'6px 0'}}/>
          <button onClick={()=>fire()} disabled={loading}
            style={{background:loading?'rgba(229,9,20,.4)':'linear-gradient(135deg,#e50914,#ff4444)',color:'#fff',border:'none',padding:'11px 24px',borderRadius:10,fontWeight:700,fontSize:'.88rem',cursor:loading?'not-allowed':'pointer',display:'flex',alignItems:'center',gap:7,flexShrink:0,whiteSpace:'nowrap'}}>
            {loading?<><Spinner/> Thinking…</>:<><I.Sparkle/> Recommend</>}
          </button>
        </div>

        {/* Chips */}
        <div style={{marginTop:'1rem',display:'flex',flexWrap:'wrap',gap:7,justifyContent:'center'}}>
          {SUGGESTIONS.map(s=>(
            <button key={s} onClick={()=>fire(s)} className="chip-hover"
              style={{background:'rgba(255,255,255,.04)',border:'1px solid rgba(255,255,255,.09)',color:'rgba(255,255,255,.55)',padding:'5px 13px',borderRadius:50,fontSize:'.73rem',cursor:'pointer'}}>
              {s}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}

// ─── LOADING SKELETON ─────────────────────────────────────────────────────────
function LoadingSkeleton() {
  return (
    <div style={{padding:'2rem 1.5rem',maxWidth:1280,margin:'0 auto'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,background:'rgba(229,9,20,.07)',border:'1px solid rgba(229,9,20,.18)',borderRadius:12,padding:'14px 20px',maxWidth:380,margin:'0 auto 2rem'}}>
        <span className="pulse-dot" style={{width:10,height:10,background:'#e50914',borderRadius:'50%',flexShrink:0}}/>
        <div>
          <div style={{color:'#ff7070',fontWeight:700,fontSize:'.85rem'}}>AI Agent Reasoning…</div>
          <div style={{color:'rgba(255,255,255,.35)',fontSize:'.73rem',marginTop:2}}>Thought → Action → Observation → Answer</div>
        </div>
      </div>
      <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:18}}>
        {[1,2,3,4,5].map(i=><div key={i} className="shimmer" style={{borderRadius:12,height:310}}/>)}
      </div>
    </div>
  );
}

// ─── REACT TRACE ─────────────────────────────────────────────────────────────
function ReactTrace({trace,query}) {
  const [open,setOpen] = useState(true);
  if(!trace?.length) return null;
  return (
    <div style={{padding:'0 1.5rem 3rem',maxWidth:900,margin:'0 auto'}}>
      <button onClick={()=>setOpen(!open)}
        style={{width:'100%',background:'rgba(255,255,255,.03)',border:'1px solid rgba(255,255,255,.08)',color:'#fff',
          padding:'13px 18px',borderRadius:open?'12px 12px 0 0':'12px',
          display:'flex',alignItems:'center',justifyContent:'space-between',cursor:'pointer',fontSize:'.95rem',fontWeight:700}}>
        <span style={{display:'flex',alignItems:'center',gap:9}}>
          <I.Brain/>
          <span>ReAct Agent Trace</span>
          <span style={{background:'rgba(229,9,20,.18)',color:'#ff7070',padding:'2px 9px',borderRadius:20,fontSize:'.7rem'}}>{trace.length} step{trace.length!==1?'s':''}</span>
        </span>
        <span style={{transform:open?'rotate(180deg)':'none',transition:'transform .2s'}}><I.Down/></span>
      </button>
      {open && (
        <div style={{background:'rgba(7,7,20,.9)',border:'1px solid rgba(255,255,255,.07)',borderTop:'none',borderRadius:'0 0 12px 12px',overflow:'hidden',backdropFilter:'blur(12px)'}}>
          <div style={{padding:'12px 18px',borderBottom:'1px solid rgba(255,255,255,.05)',background:'rgba(255,255,255,.02)',fontSize:'.8rem'}}>
            <span style={{color:'rgba(255,255,255,.35)'}}>Query: </span>
            <span style={{color:'#fff',fontWeight:600}}>"{query}"</span>
          </div>
          {trace.map((step,i)=>(
            <div key={i} className="slide-in" style={{padding:'18px',borderBottom:i<trace.length-1?'1px solid rgba(255,255,255,.04)':'none',animationDelay:`${i*0.1}s`}}>
              {/* Thought */}
              <div style={{background:'rgba(99,102,241,.09)',border:'1px solid rgba(99,102,241,.22)',borderRadius:9,padding:'10px 14px',marginBottom:9}}>
                <div style={{color:'#a5b4fc',fontSize:'.67rem',fontWeight:700,textTransform:'uppercase',letterSpacing:'.5px',marginBottom:5}}>🧠 Thought</div>
                <div style={{color:'rgba(255,255,255,.7)',fontSize:'.8rem',lineHeight:1.55}}>{step.thought}</div>
              </div>
              {/* Action */}
              <div style={{background:'rgba(229,9,20,.09)',border:'1px solid rgba(229,9,20,.22)',borderRadius:9,padding:'10px 14px',marginBottom:9}}>
                <div style={{color:'#ff7070',fontSize:'.67rem',fontWeight:700,textTransform:'uppercase',letterSpacing:'.5px',marginBottom:5}}>⚡ Action → {step.action}</div>
                <pre style={{color:'rgba(255,255,255,.65)',fontSize:'.73rem',fontFamily:'monospace',margin:0,overflowX:'auto',whiteSpace:'pre-wrap',wordBreak:'break-word'}}>
                  {typeof step.action_input==='object'?JSON.stringify(step.action_input,null,2):String(step.action_input)}
                </pre>
              </div>
              {/* Observation */}
              <div style={{background:'rgba(16,185,129,.08)',border:'1px solid rgba(16,185,129,.22)',borderRadius:9,padding:'10px 14px'}}>
                <div style={{color:'#6ee7b7',fontSize:'.67rem',fontWeight:700,textTransform:'uppercase',letterSpacing:'.5px',marginBottom:5}}>👁 Observation</div>
                <pre style={{color:'rgba(255,255,255,.6)',fontSize:'.72rem',fontFamily:'monospace',margin:0,overflowX:'auto',whiteSpace:'pre-wrap',maxHeight:180,overflowY:'auto'}}>
                  {step.observation}
                </pre>
              </div>
            </div>
          ))}
          <div style={{padding:'12px 18px',background:'rgba(99,102,241,.06)',borderTop:'1px solid rgba(99,102,241,.15)'}}>
            <span style={{color:'#a5b4fc',fontWeight:700,fontSize:'.82rem'}}>✅ Final Answer Generated</span>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── RESULTS SECTION ─────────────────────────────────────────────────────────
function FilterBadge({label}) {
  return <span style={{background:'rgba(229,9,20,.1)',border:'1px solid rgba(229,9,20,.22)',color:'#ff7070',padding:'3px 11px',borderRadius:20,fontSize:'.7rem',fontWeight:600}}>{label}</span>;
}

function ResultsSection({data}) {
  const {movies=[],user_movies=[],final_answer,constraints={},elapsed_seconds,mode,sources={}} = data;

  return (
    <div style={{padding:'2rem 1.5rem',maxWidth:1280,margin:'0 auto'}}>
      {/* Meta bar */}
      <div style={{display:'flex',flexWrap:'wrap',gap:12,alignItems:'center',marginBottom:'1.5rem',justifyContent:'space-between'}}>
        <div>
          <h2 style={{fontSize:'1.4rem',fontWeight:900,marginBottom:4}}>
            Found <span style={{color:'#e50914'}}>{movies.length} TMDB</span>
            {user_movies.length>0&&<> + <span style={{color:'#ffa500'}}>{user_movies.length} My Movies</span></>}
          </h2>
          <div style={{color:'rgba(255,255,255,.35)',fontSize:'.78rem',display:'flex',gap:14,flexWrap:'wrap'}}>
            <span>⚡ {elapsed_seconds}s</span>
            <span>📡 {mode==='react_agent'?'ReAct Agent':'TMDB Direct'}</span>
            {sources.live_tmdb_count>0 && <span style={{color:'#01b4e4'}}>🔴 Live: {sources.live_tmdb_count}</span>}
            {sources.db_cache_count>0  && <span>💾 Cache: {sources.db_cache_count}</span>}
            {sources.user_count>0      && <span style={{color:'#ffa500'}}>👤 Yours: {sources.user_count}</span>}
          </div>
        </div>
        <div style={{display:'flex',flexWrap:'wrap',gap:6}}>
          {constraints.genre_name && <FilterBadge label={`Genre: ${constraints.genre_name}`}/>}
          {constraints.year_gte && <FilterBadge label={`${constraints.year_gte}–${constraints.year_lte||'now'}`}/>}
          {constraints.certification && <FilterBadge label={`Rated ${constraints.certification}`}/>}
          {constraints.min_rating && <FilterBadge label={`⭐ >${constraints.min_rating}`}/>}
          {constraints.language && <FilterBadge label={`Lang: ${constraints.language}`}/>}
        </div>
      </div>

      {/* User movies (highlighted section) */}
      {user_movies.length>0 && (
        <div style={{marginBottom:'2rem'}}>
          <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:'1rem'}}>
            <span style={{fontSize:'.9rem',fontWeight:800,color:'#ffa500'}}>👤 From Your Collection</span>
            <span style={{background:'rgba(255,165,0,.12)',border:'1px solid rgba(255,165,0,.25)',color:'#ffa500',padding:'2px 9px',borderRadius:20,fontSize:'.67rem',fontWeight:700}}>{user_movies.length} match{user_movies.length!==1?'es':''}</span>
          </div>
          <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:16}}>
            {user_movies.map((m,i)=><MovieCard key={`u-${m.id||i}`} movie={m} index={i} showSource/>)}
          </div>
        </div>
      )}

      {/* TMDB movies */}
      {movies.length>0 && (
        <>
          {user_movies.length>0 && (
            <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:'1rem'}}>
              <span style={{fontSize:'.9rem',fontWeight:800,color:'#01b4e4'}}>🎬 From TMDB</span>
            </div>
          )}
          <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:18,marginBottom:'2rem'}}>
            {movies.map((m,i)=><MovieCard key={`t-${m.id||m.tmdb_id||i}`} movie={m} index={i} showSource={user_movies.length>0}/>)}
          </div>
        </>
      )}

      {/* AI Summary */}
      {final_answer && (
        <div style={{background:'rgba(229,9,20,.05)',border:'1px solid rgba(229,9,20,.18)',borderRadius:14,padding:'1.25rem 1.5rem'}}>
          <div style={{display:'flex',alignItems:'center',gap:7,marginBottom:10}}>
            <I.Brain/>
            <span style={{fontWeight:700,color:'#ff7070',fontSize:'.85rem'}}>Agent Summary</span>
          </div>
          <p style={{color:'rgba(255,255,255,.65)',lineHeight:1.7,fontSize:'.88rem',whiteSpace:'pre-line'}}>{final_answer}</p>
        </div>
      )}
    </div>
  );
}

// ─── MY MOVIES TAB ───────────────────────────────────────────────────────────
function MyMoviesPanel({onAddMovie,onRateMovie}) {
  const [movies,setMovies]   = useState([]);
  const [loading,setLoading] = useState(true);

  const load = useCallback(async()=>{
    setLoading(true);
    try {
      const {data} = await axios.get(`${API}/movies/user`);
      setMovies(data.movies||[]);
    } catch(e) { console.error(e); }
    setLoading(false);
  },[]);

  useEffect(()=>{load();},[load]);

  return (
    <div style={{padding:'2rem 1.5rem',maxWidth:1280,margin:'0 auto'}}>
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'1.5rem',flexWrap:'wrap',gap:12}}>
        <div>
          <h2 style={{fontSize:'1.5rem',fontWeight:900}}>👤 My Movie Collection</h2>
          <p style={{color:'rgba(255,255,255,.4)',fontSize:'.83rem',marginTop:3}}>{movies.length} movie{movies.length!==1?'s':''} — all searchable by the AI agent</p>
        </div>
        <div style={{display:'flex',gap:8}}>
          <button onClick={onAddMovie} style={{background:'rgba(255,165,0,.1)',border:'1px solid rgba(255,165,0,.3)',color:'#ffa500',padding:'8px 16px',borderRadius:9,fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:5,fontSize:'.82rem'}}><I.Plus/> Add Movie</button>
          <button onClick={onRateMovie} style={{background:'rgba(168,85,247,.1)',border:'1px solid rgba(168,85,247,.3)',color:'#c084fc',padding:'8px 16px',borderRadius:9,fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:5,fontSize:'.82rem'}}><I.Wand/> Rate Movie</button>
        </div>
      </div>

      {loading ? (
        <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:18}}>
          {[1,2,3,4].map(i=><div key={i} className="shimmer" style={{borderRadius:12,height:310}}/>)}
        </div>
      ) : movies.length===0 ? (
        <div style={{textAlign:'center',padding:'5rem 1rem'}}>
          <div style={{fontSize:'4rem',marginBottom:'1rem'}}>🎬</div>
          <h3 style={{fontSize:'1.2rem',fontWeight:700,marginBottom:8}}>No movies yet</h3>
          <p style={{color:'rgba(255,255,255,.4)',marginBottom:'1.5rem'}}>Add your own movies or rate any film to build your collection.</p>
          <div style={{display:'flex',gap:10,justifyContent:'center',flexWrap:'wrap'}}>
            <button onClick={onAddMovie} style={{background:'linear-gradient(135deg,#e50914,#ff4444)',color:'#fff',border:'none',padding:'11px 24px',borderRadius:50,fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:6}}><I.Plus/> Add My Movie</button>
            <button onClick={onRateMovie} style={{background:'linear-gradient(135deg,#7c3aed,#a855f7)',color:'#fff',border:'none',padding:'11px 24px',borderRadius:50,fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:6}}><I.Wand/> Rate My Movie</button>
          </div>
        </div>
      ) : (
        <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:18}}>
          {movies.map((m,i)=><MovieCard key={m.id||i} movie={m} index={i} showSource/>)}
        </div>
      )}
    </div>
  );
}

// ─── BROWSE DB TAB ────────────────────────────────────────────────────────────
function BrowseDBPanel() {
  const [movies,setMovies]   = useState([]);
  const [loading,setLoading] = useState(true);
  const [page,setPage]       = useState(1);
  const [total,setTotal]     = useState(0);
  const [totalPages,setTotalPages] = useState(1);
  const [filter,setFilter]   = useState({genre:'',year_gte:'',year_lte:'',min_rating:''});
  const [fetching,setFetching] = useState(false);
  const [dbReady,setDbReady]   = useState(false);

  const load = useCallback(async(p=1)=>{
    setLoading(true);
    try {
      const params = {page:p,per_page:20};
      if(filter.genre)      params.genre=filter.genre;
      if(filter.year_gte)   params.year_gte=filter.year_gte;
      if(filter.year_lte)   params.year_lte=filter.year_lte;
      if(filter.min_rating) params.min_rating=filter.min_rating;
      const {data} = await axios.get(`${API}/movies/db`,{params});
      setMovies(data.movies||[]); setTotal(data.total||0);
      setTotalPages(data.total_pages||1); setPage(p);
      setDbReady(data.db_fetch_complete);
    } catch(e) { console.error(e); }
    setLoading(false);
  },[filter]);

  useEffect(()=>{load(1);},[load]);

  const genres=['Action','Adventure','Animation','Comedy','Crime','Drama','Family','Fantasy','Horror','Music','Mystery','Romance','Science Fiction','Thriller','War','Western'];

  return (
    <div style={{padding:'2rem 1.5rem',maxWidth:1280,margin:'0 auto'}}>
      <div style={{marginBottom:'1.5rem'}}>
        <h2 style={{fontSize:'1.5rem',fontWeight:900,marginBottom:4}}>🎬 Movie Database
          <span style={{fontWeight:400,fontSize:'1rem',color:'rgba(255,255,255,.35)',marginLeft:10}}>{total} movies</span>
          {!dbReady && <span style={{marginLeft:10,background:'rgba(229,9,20,.12)',border:'1px solid rgba(229,9,20,.25)',color:'#ff7070',padding:'2px 9px',borderRadius:20,fontSize:'.65rem',fontWeight:700}}>⟳ Fetching…</span>}
        </h2>
        <p style={{color:'rgba(255,255,255,.4)',fontSize:'.83rem'}}>100+ real movies from TMDB — fetched, cached, and searchable</p>
      </div>

      {/* Filters */}
      <div style={{display:'flex',gap:10,flexWrap:'wrap',marginBottom:'1.5rem',alignItems:'center'}}>
        <select value={filter.genre} onChange={e=>{setFilter(f=>({...f,genre:e.target.value}));}}
          style={{background:'rgba(255,255,255,.05)',border:'1px solid rgba(255,255,255,.1)',color:filter.genre?'#fff':'rgba(255,255,255,.4)',padding:'7px 14px',borderRadius:9,fontSize:'.82rem',cursor:'pointer'}}>
          <option value="" style={{background:'#12122a'}}>All Genres</option>
          {genres.map(g=><option key={g} value={g} style={{background:'#12122a'}}>{g}</option>)}
        </select>
        <input value={filter.year_gte} onChange={e=>setFilter(f=>({...f,year_gte:e.target.value}))}
          placeholder="From Year" style={{background:'rgba(255,255,255,.05)',border:'1px solid rgba(255,255,255,.1)',color:'#fff',padding:'7px 12px',borderRadius:9,fontSize:'.82rem',width:110}}/>
        <input value={filter.year_lte} onChange={e=>setFilter(f=>({...f,year_lte:e.target.value}))}
          placeholder="To Year" style={{background:'rgba(255,255,255,.05)',border:'1px solid rgba(255,255,255,.1)',color:'#fff',padding:'7px 12px',borderRadius:9,fontSize:'.82rem',width:110}}/>
        <input value={filter.min_rating} onChange={e=>setFilter(f=>({...f,min_rating:e.target.value}))}
          placeholder="Min Rating" type="number" min="0" max="10" step="0.5"
          style={{background:'rgba(255,255,255,.05)',border:'1px solid rgba(255,255,255,.1)',color:'#fff',padding:'7px 12px',borderRadius:9,fontSize:'.82rem',width:110}}/>
        <button onClick={()=>load(1)} style={{background:'linear-gradient(135deg,#e50914,#ff4444)',color:'#fff',border:'none',padding:'7px 18px',borderRadius:9,fontWeight:700,cursor:'pointer',fontSize:'.82rem'}}>Apply</button>
        <button onClick={()=>{setFilter({genre:'',year_gte:'',year_lte:'',min_rating:''});}} style={{background:'rgba(255,255,255,.06)',border:'1px solid rgba(255,255,255,.1)',color:'rgba(255,255,255,.6)',padding:'7px 14px',borderRadius:9,fontSize:'.82rem',cursor:'pointer'}}>Clear</button>
      </div>

      {loading ? (
        <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:18}}>
          {Array.from({length:12},(_,i)=><div key={i} className="shimmer" style={{borderRadius:12,height:310}}/>)}
        </div>
      ) : movies.length===0 ? (
        <div style={{textAlign:'center',padding:'4rem',color:'rgba(255,255,255,.4)'}}>
          <div style={{fontSize:'3rem',marginBottom:'1rem'}}>🔍</div>
          <p>No movies match the selected filters.</p>
        </div>
      ) : (
        <>
          <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:18,marginBottom:'2rem'}}>
            {movies.map((m,i)=><MovieCard key={m.id||m.tmdb_id||i} movie={m} index={i}/>)}
          </div>
          {/* Pagination */}
          {totalPages>1 && (
            <div style={{display:'flex',justifyContent:'center',gap:8,alignItems:'center'}}>
              <button onClick={()=>load(page-1)} disabled={page<=1}
                style={{background:'rgba(255,255,255,.06)',border:'1px solid rgba(255,255,255,.1)',color:page<=1?'rgba(255,255,255,.2)':'#fff',padding:'8px 16px',borderRadius:9,cursor:page<=1?'default':'pointer',fontSize:'.83rem'}}>← Prev</button>
              <span style={{color:'rgba(255,255,255,.5)',fontSize:'.85rem'}}>Page {page} / {totalPages}</span>
              <button onClick={()=>load(page+1)} disabled={page>=totalPages}
                style={{background:'rgba(255,255,255,.06)',border:'1px solid rgba(255,255,255,.1)',color:page>=totalPages?'rgba(255,255,255,.2)':'#fff',padding:'8px 16px',borderRadius:9,cursor:page>=totalPages?'default':'pointer',fontSize:'.83rem'}}>Next →</button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

// ─── TRENDING SECTION ─────────────────────────────────────────────────────────
function TrendingSection({movies}) {
  if(!movies.length) return null;
  return (
    <section style={{padding:'3rem 1.5rem 5rem',maxWidth:1280,margin:'0 auto'}}>
      <h2 style={{fontSize:'1.6rem',fontWeight:900,marginBottom:'1.5rem'}}>
        🔥 Trending This Week
        <span style={{color:'rgba(255,255,255,.28)',fontWeight:400,fontSize:'.9rem',marginLeft:10}}>via TMDB</span>
      </h2>
      <div className="grid-movies" style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(190px,1fr))',gap:18}}>
        {movies.slice(0,10).map((m,i)=><MovieCard key={m.id} movie={m} index={i}/>)}
      </div>
    </section>
  );
}

// ─── APP ROOT ─────────────────────────────────────────────────────────────────
export default function App() {
  const searchRef  = useRef(null);
  const resultsRef = useRef(null);

  const [activeTab,setActiveTab]   = useState('home');   // home | myMovies | browse
  const [results,setResults]       = useState(null);
  const [loading,setLoading]       = useState(false);
  const [error,setError]           = useState(null);
  const [currentQuery,setCurrentQuery] = useState('');
  const [trending,setTrending]     = useState([]);
  const [dbCount,setDbCount]       = useState(0);
  const [showAddModal,setShowAdd]  = useState(false);
  const [showRateModal,setShowRate]= useState(false);
  const [toast,setToast]           = useState(null);
  const [hasSearched,setHasSearched] = useState(false);

  // Load trending + db count
  useEffect(()=>{
    axios.get(`${API}/trending`).then(r=>setTrending(r.data.movies||[])).catch(()=>{});
    axios.get(`${API}/health`).then(r=>setDbCount(r.data.db_movie_count||0)).catch(()=>{});
  },[]);

  const scrollToSearch = () => searchRef.current?.scrollIntoView({behavior:'smooth',block:'start'});

  const showToast = (msg,type='success') => setToast({msg,type});

  const handleSearch = useCallback(async(query,useAgent)=>{
    setLoading(true); setError(null); setResults(null);
    setCurrentQuery(query); setHasSearched(true);
    setActiveTab('home');
    setTimeout(()=>resultsRef.current?.scrollIntoView({behavior:'smooth',block:'start'}),100);
    try {
      const {data} = await axios.post(`${API}/recommend`,{query,use_agent:useAgent},{timeout:90000});
      setResults(data);
    } catch(e) {
      const msg = e.response?.data?.detail||e.message||'Something went wrong.';
      setError(msg);
    } finally { setLoading(false); }
  },[]);

  const onMovieSaved = useCallback(msg=>{
    showToast(msg,'success');
    // Refresh db count
    axios.get(`${API}/health`).then(r=>setDbCount(r.data.db_movie_count||0)).catch(()=>{});
  },[]);

  // Tab buttons
  const tabs = [
    {id:'home',    label:'🏠 Home'},
    {id:'browse',  label:'🎬 Browse DB'},
    {id:'myMovies',label:'👤 My Movies'},
  ];

  return (
    <>
      <style>{STYLES}</style>

      {toast && <Toast msg={toast.msg} type={toast.type} onClose={()=>setToast(null)}/>}
      {showAddModal  && <AddMovieModal  onClose={()=>setShowAdd(false)}  onSaved={onMovieSaved}/>}
      {showRateModal && <RateMovieModal onClose={()=>setShowRate(false)} onSaved={onMovieSaved}/>}

      <Navbar onAddMovie={()=>setShowAdd(true)} onRateMovie={()=>setShowRate(true)}
              onScrollSearch={scrollToSearch} dbCount={dbCount}/>

      {/* Tab bar */}
      <div style={{position:'sticky',top:64,zIndex:800,background:'rgba(7,7,16,.95)',backdropFilter:'blur(14px)',borderBottom:'1px solid rgba(255,255,255,.06)',display:'flex',gap:4,padding:'0 1.5rem',height:46,alignItems:'center'}}>
        {tabs.map(t=>(
          <button key={t.id} onClick={()=>setActiveTab(t.id)}
            className={activeTab===t.id?'tab-active':'tab-inactive'}
            style={{padding:'5px 16px',borderRadius:8,border:'none',fontWeight:600,fontSize:'.8rem',cursor:'pointer',transition:'all .2s'}}>
            {t.label}
          </button>
        ))}
        <div style={{marginLeft:'auto',display:'flex',gap:6}}>
          <button onClick={()=>setShowAdd(true)} style={{background:'rgba(255,165,0,.1)',border:'1px solid rgba(255,165,0,.3)',color:'#ffa500',padding:'5px 12px',borderRadius:7,fontWeight:700,fontSize:'.75rem',cursor:'pointer',display:'flex',alignItems:'center',gap:4}}>
            <I.Plus/> Add
          </button>
          <button onClick={()=>setShowRate(true)} style={{background:'rgba(168,85,247,.1)',border:'1px solid rgba(168,85,247,.3)',color:'#c084fc',padding:'5px 12px',borderRadius:7,fontWeight:700,fontSize:'.75rem',cursor:'pointer',display:'flex',alignItems:'center',gap:4}}>
            <I.Wand/> Rate
          </button>
        </div>
      </div>

      <main>
        {activeTab==='browse'   && <BrowseDBPanel/>}
        {activeTab==='myMovies' && <MyMoviesPanel onAddMovie={()=>setShowAdd(true)} onRateMovie={()=>setShowRate(true)}/>}

        {activeTab==='home' && (
          <>
            <Hero trending={trending} onScroll={scrollToSearch}
                  onAddMovie={()=>setShowAdd(true)} onRateMovie={()=>setShowRate(true)} dbCount={dbCount}/>
            <SearchSection searchRef={searchRef} onSearch={handleSearch} loading={loading}/>

            <div ref={resultsRef}>
              {loading && <LoadingSkeleton/>}

              {error && !loading && (
                <div style={{maxWidth:680,margin:'2rem auto',background:'rgba(229,9,20,.08)',border:'1px solid rgba(229,9,20,.25)',borderRadius:12,padding:'14px 18px',display:'flex',justifyContent:'space-between',alignItems:'flex-start',gap:10}}>
                  <div>
                    <div style={{color:'#ff7070',fontWeight:700,marginBottom:3}}>⚠ Error</div>
                    <div style={{color:'rgba(255,255,255,.65)',fontSize:'.85rem'}}>{error}</div>
                    {error.includes('OpenAI')&&<div style={{color:'rgba(255,255,255,.35)',fontSize:'.75rem',marginTop:4}}>Tip: Switch to ⚡ TMDB Direct mode — no OpenAI key needed.</div>}
                  </div>
                  <button onClick={()=>setError(null)} style={{background:'none',border:'none',color:'rgba(255,255,255,.4)',cursor:'pointer',flexShrink:0}}><I.X/></button>
                </div>
              )}

              {results && !loading && (
                <>
                  {(results.movies||[]).length===0 && (results.user_movies||[]).length===0
                    ? <div style={{textAlign:'center',padding:'5rem 1rem'}}>
                        <div style={{fontSize:'3.5rem',marginBottom:'1rem'}}>🎬</div>
                        <h3 style={{fontSize:'1.3rem',fontWeight:700,marginBottom:8}}>No Movies Found</h3>
                        <p style={{color:'rgba(255,255,255,.4)'}}>Try relaxing filters — wider year range, different genre, or remove certification.</p>
                      </div>
                    : <ResultsSection data={results}/>
                  }
                  <ReactTrace trace={results.trace} query={currentQuery}/>
                </>
              )}

              {!hasSearched && !loading && <TrendingSection movies={trending}/>}
            </div>
          </>
        )}
      </main>

      <footer style={{borderTop:'1px solid rgba(255,255,255,.05)',padding:'1.5rem',textAlign:'center',color:'rgba(255,255,255,.22)',fontSize:'.75rem'}}>
        <p><span style={{color:'#e50914',fontWeight:700}}>CineAI</span> · LangChain ReAct · FastAPI · React · SQLite · TMDB</p>
        <p style={{marginTop:4}}>Movie data by <a href="https://www.themoviedb.org" target="_blank" rel="noopener noreferrer" style={{color:'rgba(255,255,255,.35)',textDecoration:'none'}}>TMDB</a></p>
      </footer>
    </>
  );
}
