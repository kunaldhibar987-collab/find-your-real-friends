async function api(path, options={}) {
  const base = (window.APP_CONFIG && window.APP_CONFIG.API_BASE) || '/api';
  const res = await fetch(base + path, {headers:{'Content-Type':'application/json',...(options.headers||{})}, ...options});
  const data = await res.json().catch(()=>({detail:'Server returned an invalid response.'}));
  if(!res.ok) throw new Error(data.detail || 'Something went wrong.');
  return data;
}
function getCreatorToken(){return localStorage.getItem('creatorToken') || ''}
function ensureCreatorToken(){let t=getCreatorToken();if(!t){t='creator-'+crypto.randomUUID();localStorage.setItem('creatorToken',t)}return t}
function escapeHtml(v){return String(v??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
