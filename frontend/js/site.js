document.addEventListener('DOMContentLoaded',()=>{
 const b=document.getElementById('mobileMenuButton'), n=document.getElementById('mobileNavigation');
 if(b&&n){b.addEventListener('click',e=>{e.stopPropagation();const open=n.classList.toggle('is-open');b.setAttribute('aria-expanded',String(open));});document.addEventListener('click',e=>{if(n.classList.contains('is-open')&&!n.contains(e.target)&&!b.contains(e.target)){n.classList.remove('is-open');b.setAttribute('aria-expanded','false')}})}
 const y=document.getElementById('currentYear');if(y)y.textContent=new Date().getFullYear();
});
