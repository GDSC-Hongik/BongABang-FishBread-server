"use strict";(globalThis.webpackChunk=globalThis.webpackChunk||[]).push([["scanning"],{70763:(e,t,n)=>{n.d(t,{O4:()=>f,jo:()=>u,Qp:()=>d});var r=n(81574),o=n(59753);let s="ontransitionend"in window;function i(e){return"height"===getComputedStyle(e).transitionProperty}function l(e,t){e.style.transition="none",t(),e.offsetHeight,e.style.transition=""}var a=n(96776);function c(e,t){if(e.classList.toggle("open",t),e.classList.toggle("Details--on",t),t){let t=e.querySelector(".js-details-initial-focus");t&&setTimeout(()=>{t.focus()},0)}for(let n of[...e.querySelectorAll(".js-details-target")].filter(t=>t.closest(".js-details-container")===e))n.setAttribute("aria-expanded",t.toString())}function d(e,t){let n=e.getAttribute("data-details-container")||".js-details-container",r=e.closest(n),o=t?.force??!r.classList.contains("open"),d=t?.withGroup??!1;!function(e,t){if(!s){t();return}let n=Array.from(e.querySelectorAll(".js-transitionable"));for(let t of(e.classList.contains("js-transitionable")&&n.push(e),n)){let e=i(t);t instanceof HTMLElement&&(t.addEventListener("transitionend",()=>{t.style.display="",t.style.visibility="",e&&l(t,function(){t.style.height=""})},{once:!0}),t.style.boxSizing="content-box",t.style.display="block",t.style.visibility="visible",e&&l(t,function(){t.style.height=getComputedStyle(t).height}),t.offsetHeight)}for(let e of(t(),n))if(e instanceof HTMLElement&&i(e)){let t=getComputedStyle(e).height;e.style.boxSizing="","0px"===t?e.style.height=`${e.scrollHeight}px`:e.style.height="0px"}}(r,()=>{c(r,o);let t=d?function(e,t){let n=e.getAttribute("data-details-container-group");return n?((0,a.uQ)(e,()=>{for(let r of[...document.querySelectorAll(".js-details-container")].filter(e=>e.getAttribute("data-details-container-group")===n))r!==e&&c(r,t)}),n):null}(r,o):null;Promise.resolve().then(()=>{!function(e,t){t.find(t=>{let n=Array.from(e.querySelectorAll(t)),r=n.findLast(e=>"none"!==window.getComputedStyle(e).display);if(r&&document.activeElement!==r)return r.focus(),!0})}(r,[".js-focus-on-dismiss","input[autofocus], textarea[autofocus]"]),e.classList.contains("tooltipped")&&(e.classList.remove("tooltipped"),e.addEventListener("mouseleave",()=>{e.classList.add("tooltipped"),e.blur()},{once:!0})),r.dispatchEvent(new CustomEvent("details:toggled",{bubbles:!0,cancelable:!1,detail:{open:o}})),t&&r.dispatchEvent(new CustomEvent("details:toggled-group",{bubbles:!0,cancelable:!1,detail:{open:o,group:t}}))})})}function u(e){let t=e.getAttribute("data-details-container")||".js-details-container",n=e.closest(t),r=n.classList;return r.contains("Details--on")||r.contains("open")}function f(e){let t=!1,n=e.parentElement;for(;n;)n.classList.contains("Details-content--shown")&&(t=!0),n.classList.contains("js-details-container")&&(n.classList.toggle("open",!t),n.classList.toggle("Details--on",!t),t=!1),n=n.parentElement}(0,o.on)("click",".js-details-target",function(e){let t=e.altKey,n=e.currentTarget;d(n,{withGroup:t}),e.preventDefault()}),(0,r.Z)(function({target:e}){e&&f(e)})},81574:(e,t,n)=>{n.d(t,{Z:()=>l});var r=n(4412),o=n(55908);let s=[],i=0;function l(e){!async function(){s.push(e),await r.x,function(){let e=i;i=s.length,a(s.slice(e),null,window.location.href)}()}()}function a(e,t,n){let r=window.location.hash.slice(1),o=r?document.getElementById(r):null,s={oldURL:t,newURL:n,target:o};for(let t of e)t.call(null,s)}l.clear=()=>{s.length=i=0};let c=window.location.href;window.addEventListener("popstate",function(){c=window.location.href}),window.addEventListener("hashchange",function(e){let t=window.location.href;try{a(s,e.oldURL||c,t)}finally{c=t}});let d=null;document.addEventListener(o.Q.START,function(){d=window.location.href}),document.addEventListener(o.Q.SUCCESS,function(){a(s,d,window.location.href)})},254:(e,t,n)=>{n.d(t,{ZG:()=>l,q6:()=>c,w4:()=>a});var r=n(8439);let o=!1,s=new r.Z;function i(e){let t=e.target;if(t instanceof HTMLElement&&t.nodeType!==Node.DOCUMENT_NODE)for(let e of s.matches(t))e.data.call(null,t)}function l(e,t){o||(o=!0,document.addEventListener("focus",i,!0)),s.add(e,t),document.activeElement instanceof HTMLElement&&document.activeElement.matches(e)&&t(document.activeElement)}function a(e,t,n){function r(t){let o=t.currentTarget;o&&(o.removeEventListener(e,n),o.removeEventListener("blur",r))}l(t,function(t){t.addEventListener(e,n),t.addEventListener("blur",r)})}function c(e,t){function n(e){let{currentTarget:r}=e;r&&(r.removeEventListener("input",t),r.removeEventListener("blur",n))}l(e,function(e){e.addEventListener("input",t),e.addEventListener("blur",n)})}},35158:(e,t,n)=>{var r=n(59753);(0,r.on)("click",".js-scanning-reopen-button-disabled",function(e){e.preventDefault()}),(0,r.on)("change",".js-scanning-alert-check",function({currentTarget:e}){let t=e.closest(".js-scanning-alert-list"),n=null!=t.querySelector(".js-scanning-alert-check:checked"),r=t.querySelector(".js-scanning-filter-options"),o=t.querySelector(".js-scanning-alert-bulk-actions"),s=t.querySelector(".js-scanning-alert-links");r&&(r.style.visibility=n?"hidden":"visible"),o&&(o.hidden=!n),s&&(s.style.visibility=n?"hidden":"visible"),function(e){let t=!1,n=e.querySelectorAll(".js-scanning-fixed-alert-numbers"),r=0!==n.length?JSON.parse(n[0].getAttribute("data-numbers")||"[]"):[];for(let n of e.querySelectorAll(".js-scanning-bulk-action-items")){n.textContent="";let o=e.querySelectorAll(".js-scanning-alert-list [data-check-all-item]:checked");for(let e of o)t||(t=-1!==r.indexOf(parseInt(e.value))),n.appendChild(function(e){let t=document.createElement("input");return t.setAttribute("type","hidden"),t.setAttribute("name",e.name),t.setAttribute("value",e.value),t}(e))}for(let n of e.querySelectorAll(".js-scanning-reopen-button"))n.hidden=t;for(let n of e.querySelectorAll(".js-scanning-reopen-button-disabled"))n.hidden=!t}(t)}),(0,r.on)("click",".js-scanning-code-path-menu-item",function(e){if(null===e.currentTarget||!(e.currentTarget instanceof Element))return;let t=e.currentTarget.getAttribute("data-target-code-path");for(let e of document.querySelectorAll(".js-scanning-code-path-menu-item"))e.ariaChecked="false";for(let n of(e.currentTarget.ariaChecked="true",document.querySelectorAll(".js-scanning-code-path")))n.hidden=t!==n.getAttribute("data-code-path")},{capture:!0})},49657:(e,t,n)=>{function r(){document.removeEventListener("turbo:load",r);let e=document.querySelector('[data-target="secret-scanning-filter.clearButton"]');if(null===e)return;let t=e?.hidden;if(t){let e=document.querySelectorAll(".js-change-open-close-state"),t=e[e.length-2];t?.focus();return}document.title=document.title.concat(" (filters applied)"),e.focus()}(0,n(59753).on)("click",".js-change-open-close-state",function(){document.addEventListener("turbo:load",r)})},16560:(e,t,n)=>{n(35158);var r=n(59753),o=n(254),s=n(69567),i=n(46263),l=n(36071),a=n(18699),c=n(57619),d=n(70763);function u(e){return e.currentTarget}function f(e){e.textContent=e.getAttribute("data-disable-with")||"",e.disabled=!0}function m(e){e.textContent=e.getAttribute("data-original-text")||"",e.disabled=!1}function p(){return document.querySelector(".js-custom-secret-scanning-pattern-form")}(0,l.N7)(".js-add-secret-format-button",{add(){window.postProcessingExpressionCount=0;let e=document.querySelector(".js-post-processing-expression-count");e&&e.textContent&&(window.postProcessingExpressionCount=parseInt(e.textContent))}}),(0,r.on)("click",".js-add-secret-format-button",e=>{let t=e.currentTarget;if(t&&window.postProcessingExpressionCount<_()){let e=document.querySelectorAll(".js-additional-secret-format");if(!e)return;for(let n of e)if(n.classList.contains("has-removed-contents")){n.classList.toggle("has-removed-contents",!1),window.postProcessingExpressionCount++,window.postProcessingExpressionCount===_()&&(t.hidden=!0);break}}}),(0,r.on)("click",".js-remove-secret-format-button",e=>{let t=document.querySelector(".js-add-secret-format-button");if(!t)return;let n=e.currentTarget;if(!n)return;let r=n.closest(".js-additional-secret-format");if(!r)return;r.classList.toggle("has-removed-contents",!0);let o=r.getElementsByClassName("js-post-processing-input")[0];o.value="";let s=Array.from(r.getElementsByClassName("js-post-processing-input-rule")),i=r.getElementsByClassName("errored")[0];for(let e of(i&&i.classList.toggle("errored",!1),s))document.getElementById(`${e.id}_hidden`)?.remove();document.getElementById(`${o.id}_hidden`)?.remove(),y(window.codeEditor.getValue()),window.postProcessingExpressionCount--,window.postProcessingExpressionCount<_()&&(t.hidden=!1)}),(0,l.N7)(".js-test-code",{async add(){let e=document.querySelector(".js-test-code"),t=e.clientHeight,r=await n.e("vendors-node_modules_codemirror_lib_codemirror_js").then(n.t.bind(n,4631,23));if(window.codeEditor=r.default.fromTextArea(e,{lineNumbers:!1,lineWrapping:!0,mode:"text/x-yaml",inputStyle:"contenteditable",value:e.value,lineSeparator:"\r\n",theme:"github-light"}),0!==t){let e=document.querySelector(".CodeMirror");e&&(e.style.height=`${t}px`,e.style.border="1px solid #e1e4e8",e.style.borderRadius="6px")}window.codeEditor.save();let o=document.querySelector(".js-test-custom-secret-scanning-pattern");if(!o)return;let s=y;o.hasAttribute("data-source-is-readonly")&&(s=x),window.codeEditor.on("change",()=>{s(window.codeEditor.getValue())})}}),(0,r.on)("change",".js-post-processing-input-rule",async function(){/^((?!chrome|android).)*safari/i.test(navigator.userAgent)&&window.codeEditor&&y(window.codeEditor.getValue())}),(0,o.q6)(".js-custom-secret-scanning-pattern-form *",async function(){window.codeEditor&&y(window.codeEditor.getValue())}),(0,r.on)("click",".js-repo-selector-dialog-summary-button.disabled",e=>{e.preventDefault()}),(0,o.q6)(".js-description-input",async function(){let e=document.querySelector(".js-description-input");if(!e)return;v(e.parentElement);let t=e.getAttribute("aria-describedby");document.querySelector(`#${t}`)?.remove()}),(0,r.on)("click",".js-generated-expression-use",async e=>{let t=document.querySelector(".js-secret-format");if(!t)return;let n=document.querySelector(".js-generate-expression-examples");if(!n)return;let r=e.currentTarget,o=r.attributes.getNamedItem("for")?.value,s=document.getElementById(o);s&&(t.value=s.textContent,window.codeEditor.setValue(n.value.replaceAll(`
`," ")),t.focus())}),(0,r.on)("click",".js-generate-expressions-form-submit-button",async e=>{let t;e.preventDefault();let n=document.querySelector(".js-description-input");if(!n)return;if(""===n.value){E(n.parentElement),w(n,"description_empty","Field cannot be blank");return}let r=document.querySelector(".js-generated-expressions-section");if(!r)return;let o=document.querySelector(".js-generated-expressions-error-section");if(!o)return;let s=document.querySelector(".js-generated-expressions-warning-section");if(!s)return;r.hidden=!0,o.hidden=!0,s.hidden=!0;let i=document.querySelectorAll(".js-generated-expression-box");if(!i)return;for(let e=0;e<i.length;e++)i[e].toggleAttribute("hidden",!0);let l=u(e);if(!l)return;f(l);let a=document.querySelector(".js-generate-expressions-form");if(a){try{let e=await fetch(a.action,{method:a.method,body:new FormData(a),headers:{Accept:"application/json"}});if((t=await e.json()).error_msg){t=await e.json(),o.textContent=t.error_msg,o.hidden=!1,m(l);return}}catch(e){o.textContent="Something went wrong. Please try again later.",o.hidden=!1,m(l);return}if(t&&t.generated_expressions){if(0===t.generated_expressions.length)s.textContent="No expressions were generated. Please retry with a different description.",s.hidden=!1;else{let e=document.querySelectorAll(".js-generated-expression");if(!e)return;let n=document.querySelectorAll(".js-generated-expression-explanation");if(!n)return;for(let r=0;r<t.generated_expressions.length;r++)e[r].textContent=t.generated_expressions[r].regex,n[r].textContent=t.generated_expressions[r].explanation;for(let r=t.generated_expressions.length;r<e.length;r++)e[r].textContent="",n[r].textContent="";for(let e=0;e<t.generated_expressions.length;e++)i[e].removeAttribute("hidden");o.hidden=!0,s.hidden=!0,r.hidden=!1}}m(l)}}),(0,r.on)("click",".js-save-and-dry-run-button, .js-custom-pattern-submit-button, .js-org-repo-selector-dialog-dry-run-button",e=>{e.preventDefault();let t=u(e);if(!t)return;f(t);let n=p();n&&((t.className.includes("js-save-and-dry-run-button")||t.className.includes("js-org-repo-selector-dialog-dry-run-button"))&&g(n,"submit_type","save_and_dry_run"),(0,r.f)(n,"submit"))});let g=(e,t,n)=>{let r=document.createElement("input");r.type="hidden",r.name=t,r.id=`${t}_hidden`,r.value=n,e.appendChild(r),r.required=!0},y=(0,i.D)(function(e){let t=document.querySelector(".js-custom-pattern-submit-button"),n=document.querySelector(".js-save-and-dry-run-button"),r=document.querySelector(".js-repo-selector-dialog-summary-button"),o=document.querySelector(".js-update-pattern-info"),s=document.querySelector(".js-test-pattern-matches");if(s){if(0===e.length){let e=document.querySelector(".js-dry-run-status");if(!e)return;e.textContent?.toLowerCase()==="queued"||e.textContent?.toLowerCase()==="inprogress"||t?.setAttribute("disabled","true"),n?.setAttribute("disabled","true"),r?.classList.add("disabled"),s.textContent=""}else{window.codeEditor.save();let e=document.querySelector(".js-test-custom-secret-scanning-pattern");if(!(e instanceof HTMLFormElement))return;let i=p();if(!i)return;for(let t of i.elements)if(t instanceof HTMLInputElement&&t.name&&("text"===t.type||"radio"===t.type&&t.checked)){let n=document.getElementById(`${t.name}_hidden`);null!==n&&n.remove(),g(e,t.name,t.value)}T(e,b(i,t,n,r,o),h(s))}}},300),h=e=>t=>{if(0===t.length)e.textContent=" - No matches";else if(1===t.length)e.textContent=" - 1 match";else{let n=[];for(let e of t)n.push(JSON.stringify(e));let r=new Set(n),o=[...r];e.textContent=` - ${o.length} matches`}},b=(e,t,n,r,o)=>s=>{if(function(e){let t=document.querySelector(".js-error-banner");for(let n of(t.hidden=!0,e.getElementsByTagName("input")))if(n.parentElement?.classList.contains("errored")){v(n.parentElement);let e=n.getAttribute("aria-describedby");document.querySelector(`#${e}`)?.remove()}}(e),s?.message){if(t?.setAttribute("disabled","true"),n?.setAttribute("disabled","true"),r?.classList.add("disabled"),o)o.hidden=!0;else if(s?.error_type==="START_DELIMITER"||s?.error_type==="END_DELIMITER"||s?.error_type==="MUST_MATCH"||s?.error_type==="MUST_NOT_MATCH"){let e=document.querySelector(".js-more-options.js-details-container");e&&(0,d.O4)(e)}return function(e,t){if("MUST_MATCH"===t.error_type||"MUST_NOT_MATCH"===t.error_type){let n=0,r=e.getElementsByClassName("js-additional-secret-format");for(let e of r){if(n>(t.error_index||0))return;let r=e.getElementsByTagName("input"),o=[...r].filter(e=>e.checked),s=o&&o[0]?.value.toUpperCase(),i=s===t.error_type&&n===t.error_index,l=e.getElementsByTagName("input"),a=[...l].filter(e=>"text"===e.type);if(!a||0===a.length)continue;let c=a[0];if(""!==c.value){if(i){let e=c.id;c&&c.parentElement&&(E(c.parentElement),w(c,e,t.message,!0,"mt-6"));return}s===t.error_type&&n++}}}else{let e=j[t.error_type],n=document.querySelector(`#${e}`);n&&n.parentElement&&(E(n.parentElement),w(n,e,t.message,!0))}}(e,s),!1}{let e=document.querySelector(".js-mode");if(!e)return!1;let s=document.querySelector(".js-dry-run-status");return!!s&&(s.textContent?.toLowerCase()!=="cancelled"&&s.textContent?.toLowerCase()!=="skipped"&&(e.textContent?.toLowerCase()==="unpublished"||e.textContent?.toLowerCase()==="published")||t?.removeAttribute("disabled"),r?.classList.remove("disabled"),n?.removeAttribute("disabled"),o&&(o.hidden=!1),!0)}};function _(){let e=document.querySelector(".js-post-processing-expression-max-count");if(!e)return 10;let t=e.textContent;return t?parseInt(t):10}function E(e){e?.classList.add("form-group","errored","my-0")}function v(e){e?.classList.remove("form-group","errored","my-0")}function w(e,t,n,r=!1,o="mt-4"){let s=document.createElement("p"),i=`${t}_error_message`;s.classList.add("note","error"),r&&s.classList.add(o),s.id=i,s.textContent=n,e.setAttribute("aria-describedby",i),e.insertAdjacentElement("afterend",s)}function S(){if(!window.codeEditor)return;let e=window.codeEditor.posFromIndex(0),t=window.codeEditor.posFromIndex(window.codeEditor.getValue().length);for(let n of window.codeEditor.findMarks(e,t))n.clear()}let j={NONE:"",CONFIG_LOAD:"secret_format",COMPILE_DB:"secret_format",START_DELIMITER:"before_secret",END_DELIMITER:"after_secret",DISPLAY_NAME:"display_name",DB_SIZE:"secret_format",DB_SIZE_CALCULATION:"secret_format"};async function T(e,t,n){let r;try{let t=await fetch(e.action,{method:e.method,body:new FormData(e),headers:{Accept:"application/json"}});t.ok&&(r=await t.json())}catch(e){}if(r){if(t(r.error)){if(r.has_matches){let e=JSON.parse(r.matches);for(let t of(S(),n(e),e))!function(e,t,n){let r=e.getValue();if(t=(0,c.yb)(r,t),n=(0,c.yb)(r,n),-1===t||-1===n)return;let o=e.posFromIndex(t),s=e.posFromIndex(n);e.markText(o,s,{className:"text-bold hx_keyword-hl rounded-2 d-inline-block"})}(window.codeEditor,t.start,t.end)}else n([]),S()}!function(e){let t=document.querySelector(".js-wildcards-warning");t&&(t.hidden=!e)}(r.has_wildcard_warning)}}let x=(0,i.D)(function(e){let t=document.querySelector(".js-test-custom-secret-scanning-pattern");if(!(t instanceof HTMLFormElement))return;let n=document.querySelector(".js-test-pattern-matches");if(n){if(0===e.length)n.textContent="";else{if(!window.codeEditor)return;window.codeEditor.save(),T(t,()=>!0,h(n))}}},300);async function L(e){let t=e.currentTarget;e.preventDefault(),C(t,parseInt(t.remove_repo_id.value),!1)}async function A(e,t=!1){let n=document.getElementById("selected_repo_ids");if(!n)return;let r=JSON.parse(n.value),o=new Set(r);o.clear(),n.value=JSON.stringify(Array.from(o));let i=document.querySelector(".js-org-repo-selector-dialog-dry-run-button");if(!i)return;t?i.removeAttribute("disabled"):i.setAttribute("disabled","true");let l=new FormData(e);l.append("selected_repo_ids",n.value);let c=await fetch(e.action,{method:e.method,body:l,headers:{Accept:"text/fragment+html"}});if(c.status>=400){let e=document.querySelector("template.js-flash-template");e.after(new s.R(e,{className:"flash-error",message:"An unknown error occurred."}))}else if(!t){let e=document.querySelector(".js-dry-run-selected-repos"),t=(0,a.r)(document,await c.text());e.replaceWith(t)}}async function C(e,t,n){let r=document.getElementById("selected_repo_ids");if(!r)return;let o=document.querySelector(".js-org-repo-selector-dialog-dry-run-button");if(!o)return;let i=JSON.parse(r.value),l=new Set(i);n?l.size<function(){let e=document.querySelector(".js-dry-run-selected-repos-max-count");if(!e)return 10;let t=e.textContent;return t?parseInt(t):10}()&&l.add(t):l.delete(t),r.value=JSON.stringify(Array.from(l)),l.size>0?o.removeAttribute("disabled"):o.setAttribute("disabled","true");let c=new FormData(e);c.append("selected_repo_ids",r.value);let d=await fetch(e.action,{method:e.method,body:c,headers:{Accept:"text/fragment+html"}});if(d.status>=400){let e=document.querySelector("template.js-flash-template");e.after(new s.R(e,{className:"flash-error",message:"An unknown error occurred."}))}else{let e=document.querySelector(".js-dry-run-selected-repos"),t=(0,a.r)(document,await d.text());e.replaceWith(t)}}(0,r.on)("click",".js-remove-dry-run-repo-form",L),(0,r.on)("auto-complete-change",".js-dry-run-repo-autocomplete",function(e){let t=e.target;if(!t.value)return;if(t.value.includes("No repositories found.")){t.value="";return}let n=t.closest("form");C(n,parseInt(n.repo_id.value),!0),t.value=""}),(0,r.on)("click",".js-clear-selected-repositories-button",function(){let e=document.querySelector(".js-add-dry-run-repo-form");e&&A(e)}),(0,l.N7)('input[type="radio"][name="dry_run_repo_selection"]',e=>{let t=document.querySelector(".js-dry-run-repo-selection-component");t&&e&&!0===e.checked&&("all_repos"===e.value?t.hidden=!0:"selected_repos"===e.value&&(t.hidden=!1))}),(0,r.on)("click",'input[type="radio"][name="dry_run_repo_selection"]',function(e){let t=e.currentTarget,n=document.querySelector(".js-dry-run-repo-selection-component");if(n){if("all_repos"===t.value){n.hidden=!0;let e=n.querySelector("form");if(!e)return;A(e,!0)}else if("selected_repos"===t.value){n.hidden=!1;let e=document.querySelector(".js-org-repo-selector-dialog-dry-run-button");if(!e)return;let t=document.getElementById("selected_repo_ids");if(!t)return;n.children[1].childElementCount<=1?e.setAttribute("disabled","true"):e.removeAttribute("disabled")}}}),(0,o.w4)("keydown",".js-dry-run-repo-autocomplete-input",function(e){"Enter"===e.key&&e.preventDefault()}),n(49657)},95253:(e,t,n)=>{let r;n.d(t,{YT:()=>f,qP:()=>m,yM:()=>p});var o=n(88149),s=n(86058),i=n(44544),l=n(71643);let{getItem:a}=(0,i.Z)("localStorage"),c="dimension_",d=["utm_source","utm_medium","utm_campaign","utm_term","utm_content","scid"];try{let e=(0,o.n)("octolytics");delete e.baseContext,r=new s.R(e)}catch(e){}function u(e){let t=(0,o.n)("octolytics").baseContext||{};if(t)for(let[e,n]of(delete t.app_id,delete t.event_url,delete t.host,Object.entries(t)))e.startsWith(c)&&(t[e.replace(c,"")]=n,delete t[e]);let n=document.querySelector("meta[name=visitor-payload]");if(n){let e=JSON.parse(atob(n.content));Object.assign(t,e)}let r=new URLSearchParams(window.location.search);for(let[e,n]of r)d.includes(e.toLowerCase())&&(t[e]=n);return t.staff=(0,l.B)().toString(),Object.assign(t,e)}function f(e){r?.sendPageView(u(e))}function m(e,t={}){let n=document.head?.querySelector('meta[name="current-catalog-service"]')?.content,o=n?{service:n}:{};for(let[e,n]of Object.entries(t))null!=n&&(o[e]=`${n}`);if(r){let t=e||"unknown";u(o),r.sendEvent(t,u(o))}}function p(e){return Object.fromEntries(Object.entries(e).map(([e,t])=>[e,JSON.stringify(t)]))}},18699:(e,t,n)=>{n.d(t,{r:()=>l});var r=n(22490),o=n(7180);let s="parse-html-no-op",i=r.ZO.createPolicy(s,{createHTML:e=>o.O.apply({policy:()=>e,policyName:s,fallback:e,sanitize:!1,fallbackOnError:!0})});function l(e,t){let n=e.createElement("template");return n.innerHTML=i.createHTML(t),e.importNode(n.content,!0)}},55908:(e,t,n)=>{n.d(t,{Q:()=>r});let r=Object.freeze({INITIAL:"soft-nav:initial",START:"soft-nav:start",SUCCESS:"soft-nav:success",ERROR:"soft-nav:error",FRAME_UPDATE:"soft-nav:frame-update",END:"soft-nav:end",RENDER:"soft-nav:render",PROGRESS_BAR:{START:"soft-nav:progress-bar:start",END:"soft-nav:progress-bar:end"}})},57619:(e,t,n)=>{function r(e){let t=e.split("\u200D"),n=0;for(let e of t){let t=Array.from(e.split(/[\ufe00-\ufe0f]/).join("")).length;n+=t}return n/t.length}function o(e,t,n,r=!0){let o=e.value.substring(0,e.selectionEnd||0),s=e.value.substring(e.selectionEnd||0);return l(e,(o=o.replace(t,n))+(s=s.replace(t,n)),o.length,r),n}function s(e,t,n){if(null===e.selectionStart||null===e.selectionEnd)return o(e,t,n);let r=e.value.substring(0,e.selectionStart),s=e.value.substring(e.selectionEnd);return l(e,r+n+s,r.length),n}function i(e,t,n={}){let r=e.selectionEnd||0,o=e.value.substring(0,r),s=e.value.substring(r),i=""===e.value||o.match(/\n$/)?"":"\n",l=n.appendNewline?"\n":"",a=i+t+l;e.value=o+a+s;let c=r+a.length;return e.selectionStart=c,e.selectionEnd=c,e.dispatchEvent(new CustomEvent("change",{bubbles:!0,cancelable:!1})),e.focus(),a}function l(e,t,n,r=!0){e.value=t,r&&(e.selectionStart=n,e.selectionEnd=n),e.dispatchEvent(new CustomEvent("change",{bubbles:!0,cancelable:!1}))}function a(e,t){let n=[...e],r=new TextEncoder,o=new Uint8Array(4);for(let e=0;e<n.length;e++){let s=n[e],{written:i,read:l}=r.encodeInto(s,o);if(!i||!l)return -1;let a=i-l;if(0!==a&&(e<t&&(t-=a),e>=t))break}return t}n.d(t,{Om:()=>i,lp:()=>o,rq:()=>r,t4:()=>s,yb:()=>a})},7180:(e,t,n)=>{n.d(t,{O:()=>c,d:()=>TrustedTypesPolicyError});var r=n(46426),o=n(71643),s=n(94301),i=n(27856),l=n.n(i),a=n(95253);let TrustedTypesPolicyError=class TrustedTypesPolicyError extends Error{};let c={apply:function({policy:e,policyName:t,fallback:n,fallbackOnError:i=!1,sanitize:c,silenceErrorReporting:d=!1}){try{if((0,r.c)("BYPASS_TRUSTED_TYPES_POLICY_RULES"))return n;(0,o.b)({incrementKey:"TRUSTED_TYPES_POLICY_CALLED",trustedTypesPolicyName:t},!1,.1);let s=e();return c&&new Promise(e=>{let n=window.performance.now(),r=l().sanitize(s,{FORBID_ATTR:[]}),o=window.performance.now();if(s.length!==r.length){let i=Error("Trusted Types policy output sanitized"),l=i.stack?.slice(0,1e3),c=s.slice(0,250);(0,a.qP)("trusted_types_policy.sanitize",{policyName:t,output:c,stack:l,outputLength:s.length,sanitizedLength:r.length,executionTime:o-n}),e(s)}}),s}catch(e){if(e instanceof TrustedTypesPolicyError||(d||(0,s.eK)(e),(0,o.b)({incrementKey:"TRUSTED_TYPES_POLICY_ERROR",trustedTypesPolicyName:t}),!i))throw e}return n}}},22490:(e,t,n)=>{n.d(t,{ZO:()=>d});var r,o=n(86283),s=n(71643);function i(e){return()=>{throw TypeError(`The policy does not implement the function ${e}`)}}let l={createHTML:i("createHTML"),createScript:i("createScript"),createScriptURL:i("createScriptURL")},a=(r=globalThis).__TRUSTED_TYPE_POLICIES__??(r.__TRUSTED_TYPE_POLICIES__=new Map),c=globalThis.trustedTypes??{createPolicy:(e,t)=>({name:e,...l,...t})},d={createPolicy:(e,t)=>{if(a.has(e))return(0,s.b)({incrementKey:"TRUSTED_TYPES_POLICY_INITIALIZED_TWICE"}),a.get(e);{let n=Object.freeze(c.createPolicy(e,t));return a.set(e,n),n}}},u=!1;o.n4?.addEventListener("securitypolicyviolation",e=>{"require-trusted-types-for"!==e.violatedDirective||u||(console.warn(`Hi fellow Hubber!
    You're probably seeing a Report Only Trusted Types error near this message. This is intended behaviour, staff-only,
    does not impact application control flow, and is used solely for statistic collection. Unfortunately we
    can't gather these statistics without adding the above warnings to your console. Sorry about that!
    Feel free to drop by #pse-architecture if you have any additional questions about Trusted Types or CSP.`),u=!0)})}},e=>{var t=t=>e(e.s=t);e.O(0,["vendors-node_modules_dompurify_dist_purify_js","vendors-node_modules_stacktrace-parser_dist_stack-trace-parser_esm_js-node_modules_github_bro-a4c183","vendors-node_modules_github_selector-observer_dist_index_esm_js","vendors-node_modules_github_mini-throttle_dist_index_js-node_modules_delegated-events_dist_in-b7c06a","ui_packages_failbot_failbot_ts"],()=>t(16560)),e.O()}]);
//# sourceMappingURL=scanning-7aed27b1a9d8.js.map