#!/usr/bin/env python3
"""Navigation regressions in QuickJS with a DOM stub; no network or form submissions.
Install quickjs to run: python3 scripts/test-navigation.py.
This does not replace browser layout/accessibility testing.
"""
from pathlib import Path
import json
from urllib.parse import urljoin, urlsplit
import quickjs

root = Path(__file__).resolve().parents[1]
context = quickjs.Context()
def parse_url(value, base):
    u = urlsplit(urljoin(base, value))
    return json.dumps({'href':u.geturl(), 'origin':u.scheme+'://'+u.netloc, 'pathname':u.path, 'search':'?'+u.query if u.query else '', 'hash':'#'+u.fragment if u.fragment else ''})
context.add_callable('_parseURL', parse_url)
context.eval('''
const checks = [];
function assert(value, message) { if (!value) throw new Error(message); checks.push(message); }
class URL { constructor(value, base) { Object.assign(this, JSON.parse(_parseURL(value, base))); } }
class Element {
  constructor(attrs = {}) {
    this.attrs = attrs; this.listeners = {}; this.style = {};
    this.dataset = {}; this.offsetHeight = 76; this.offsetTop = 800;
    const values = new Set();
    this.classList = { add: x => values.add(x), remove: x => values.delete(x), contains: x => values.has(x), toggle: (x,on) => on ? values.add(x) : values.delete(x) };
  }
  get href() { return this.attrs.href || ''; }
  get target() { return this.attrs.target || ''; }
  get id() { return this.attrs.id || ''; }
  getAttribute(x) { return this.attrs[x] ?? null; }
  setAttribute(x,v) { this.attrs[x] = v; }
  hasAttribute(x) { return x in this.attrs; }
  removeAttribute(x) { delete this.attrs[x]; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() { document.activeElement = this; }
  getBoundingClientRect() { return {top: 800}; }
  fire(type, props = {}) {
    const event = {button:0, defaultPrevented:false, preventDefault() { this.defaultPrevented=true; }, ...props};
    for(const listener of this.listeners[type] || []) listener(event);
    return event;
  }
}
const burger = new Element(), nav = new Element(), header = new Element(), section = new Element({id:'lead'});
const link = new Element({href:'/#lead'}), other = new Element({href:'/pl/#lead'}), bad = new Element({href:'/#%E0%A4%A'});
const links=[link,other,bad];
const document = {
  body: new Element(), activeElement:null,
  documentElement:new Element({lang:'uk'}),
  querySelector(s) { return ({'.burger':burger,'.nav-list':nav,'.header':header})[s] || null; },
  querySelectorAll(s) {
    if(s==='a[href*="#"]' || s==='.nav-list .nav-link') return links;
    if(s==='section[id]') return [section];
    if(s.startsWith('.nav-link[href')) return [link];
    return [];
  },
  getElementById(id) { return id==='lead' ? section : null; },
  listeners:{}, addEventListener(type,fn) { this.listeners[type]=fn; }
};
const window = {
  location:new URL('https://raccoon-studio.com.ua/','https://raccoon-studio.com.ua/'),
  scrollY:0, innerWidth:390, reduced:false, listeners:{},
  history: {pushState(a,b,hash) {window.location.hash=hash;}},
  scrollTo(value) {this.lastScroll=value;},
  matchMedia() {return {matches:this.reduced};},
  addEventListener(type,fn) {(this.listeners[type] ||= []).push(fn);},
  setTimeout(fn) {fn();}
};
const navigator={userAgent:'test'};
''')
context.eval((root/'script/script.js').read_text())
context.eval('''
assert(burger.getAttribute('aria-expanded')==='false','menu starts closed');
burger.fire('click');
assert(nav.classList.contains('open') && document.body.classList.contains('modal-open'),'mobile menu opens and locks scroll');
let event = link.fire('click');
assert(event.defaultPrevented,'root-relative same-page hash handled');
assert(!nav.classList.contains('open') && !document.body.classList.contains('modal-open'),'anchor closes mobile menu');
assert(document.activeElement===section,'keyboard focus follows target');
assert(window.location.hash==='#lead' && window.lastScroll.top===704,'hash and header offset updated');
section.fire('blur');
assert(!section.hasAttribute('tabindex'),'temporary tabindex removed on blur');
assert(!other.fire('click').defaultPrevented,'cross-language link keeps native navigation');
assert(!link.fire('click',{ctrlKey:true}).defaultPrevented,'modified click keeps native navigation');
assert(!bad.fire('click').defaultPrevented,'malformed encoded hash does not throw');
window.reduced=true;link.fire('click');
assert(window.lastScroll.behavior==='auto','reduced motion respected');
window.location.pathname='/index.html';link.fire('click');
assert(window.lastScroll.top===704,'index document alias handled');
window.location.hash='#missing';window.listeners.hashchange[0]();
window.location.hash='#%E0%A4%A';window.listeners.load[0]();
assert(true,'unknown and malformed initial hashes do not throw');
burger.fire('click');document.listeners.keydown({key:'Escape'});
assert(!nav.classList.contains('open'),'Escape closes menu');
burger.fire('click');window.innerWidth=1200;window.listeners.resize[0]();
assert(burger.getAttribute('aria-expanded')==='false','desktop resize resets menu');
''')
checks=json.loads(context.eval('JSON.stringify(checks)'))
print(json.dumps({'passed':len(checks),'checks':checks},indent=2))
