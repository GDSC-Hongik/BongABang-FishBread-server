"use strict";(globalThis.webpackChunk=globalThis.webpackChunk||[]).push([["app_assets_modules_github_ref-selector_ts"],{82368:(e,t,i)=>{var s=i(70567),r=i(69567),n=i(76006),h=i(6570);function a(e,t,i,s){var r,n=arguments.length,h=n<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)h=Reflect.decorate(e,t,i,s);else for(var a=e.length-1;a>=0;a--)(r=e[a])&&(h=(n<3?r(h):n>3?r(t,i,h):r(t,i))||h);return n>3&&h&&Object.defineProperty(t,i,h),h}let o=class RefSelectorElement extends HTMLElement{connectedCallback(){window.addEventListener("resize",this.windowResized),this.refType="branch"===this.getRequiredAttr("type")?s.r.Branch:s.r.Tag;let e=this.getAttribute("current-committish");this.currentCommittish=e?atob(e):null,this.input=this.hasAttribute("initial-filter")&&this.currentCommittish||"",this.defaultBranch=atob(this.getRequiredAttr("default-branch")),this.nameWithOwner=atob(this.getRequiredAttr("name-with-owner")),this.canCreate=this.hasAttribute("can-create"),this.prefetchOnMouseover=this.hasAttribute("prefetch-on-mouseover");let t=this.getRequiredAttr("query-endpoint"),i=this.getRequiredAttr("cache-key");this.index=new s.W(this.refType,this,t,i,this.nameWithOwner),this.updateViewportSize(),this.setupFetchListeners()}disconnectedCallback(){this.resizeAnimationRequest&&cancelAnimationFrame(this.resizeAnimationRequest),window.removeEventListener("resize",this.windowResized)}updateViewportSize(){this.isMobileViewport=window.innerWidth<544,this.windowHeight=window.innerHeight}inputEntered(e){this.input=e.detail,this.render()}tabSelected(){this.index.fetchData()}renderTemplate(e,t){return new r.R(e,t,r.XK)}renderRow(e){let t=this.index.currentSearchResult[e];if(!t&&e>=this.listLength)return document.createElement("span");if(this.index.fetchFailed)return this.renderTemplate(this.fetchFailedTemplate,{index:e,refName:this.input});if(!t){let t=this.input===this.currentCommittish;return this.isCurrentVisible||(this.isCurrentVisible=t),this.renderTemplate(this.noMatchTemplate,{index:e,isCurrent:t,refName:this.input})}let i=this.input.length>0,s=t===this.currentCommittish;this.isCurrentVisible||(this.isCurrentVisible=s);let r=this.renderTemplate(this.itemTemplate,{refName:t,index:e,isFilteringClass:i?"is-filtering":"",urlEncodedRefName:this.urlEncodeRef(t),isCurrent:s,isNotDefault:t!==this.defaultBranch});if(i){let e=r.querySelector("span");e.textContent="";let i=t.split(this.input),s=i.length-1;for(let t=0;t<i.length;t++){let r=i[t];if(e.appendChild(document.createTextNode(r)),t<s){let t=document.createElement("b");t.textContent=this.input,e.appendChild(t)}}}return r}urlEncodeRef(e){return encodeURIComponent(e).replaceAll("%2F","/").replaceAll("%3A",":").replaceAll("%2B","+")}render(){if(this.currentSelectionIndex=null,!this.index.isLoading){if(!this.virtualizedList){this.index.search(this.input),this.setupVirtualizedList();return}this.listContainer.scrollTop=0,this.index.search(this.input),this.virtualizedList.setRowCount(this.listLength)}}get listHeight(){return this.isMobileViewport?.3*this.windowHeight:330}get listLength(){let e=this.index.currentSearchResult.length;return this.showCreateRow?e+1:e||1}get showCreateRow(){return!this.index.fetchFailed&&!this.index.exactMatchFound&&""!==this.input&&this.canCreate}getRequiredAttr(e,t=this){let i=t.getAttribute(e);if(!i)throw Error(`Missing attribute for ${t}: ${e}`);return i}setupFetchListeners(){let e=this.closest("details"),t=!1,i=()=>{t||(this.index.fetchData(),t=!0)};if(!e||e.open){i();return}this.prefetchOnMouseover&&e.addEventListener("mouseover",i,{once:!0}),this.addEventListener("keydown",this.keydown),this.addEventListener("change",this.updateCurrent);let s=e.querySelector("input[data-ref-filter]");s&&(s.addEventListener("input",()=>{this.input=s.value,this.render()}),s.addEventListener("keydown",t=>{if("ArrowDown"!==t.key&&("Tab"!==t.key||t.shiftKey)){if("Enter"===t.key){let i=this.index.currentSearchResult.indexOf(this.input);if(-1===i){if(!this.showCreateRow)return;i=this.listLength-1}let s=e.querySelector(`[data-index="${i}"]`);s.click(),t.preventDefault()}}else t.preventDefault(),t.stopPropagation(),this.focusFirstListMember()}))}focusFirstListMember(){this.virtualizedList&&(this.currentSelectionIndex=0,this.focusItemAtIndex(this.currentSelectionIndex))}updateCurrent(e){e.target instanceof HTMLInputElement&&e.target.checked&&e.target.value&&(this.currentCommittish=e.target.value)}keydown(e){if(null!==this.currentSelectionIndex){if("Enter"===e.key){let t=document.activeElement;if(!t)return;t.click(),e.preventDefault();return}if("Tab"!==e.key&&"Escape"!==e.key)switch(e.preventDefault(),e.stopPropagation(),e.key){case"ArrowUp":this.currentSelectionIndex--,this.currentSelectionIndex<0&&(this.currentSelectionIndex=this.listLength-1),this.focusItemAtIndex(this.currentSelectionIndex);break;case"Home":this.currentSelectionIndex=0,this.focusItemAtIndex(this.currentSelectionIndex);break;case"End":this.currentSelectionIndex=this.listLength-1,this.focusItemAtIndex(this.currentSelectionIndex);break;case"ArrowDown":this.currentSelectionIndex++,this.currentSelectionIndex>this.listLength-1&&(this.currentSelectionIndex=0),this.focusItemAtIndex(this.currentSelectionIndex)}}}focusItemAtIndex(e){this.virtualizedList.scrollToIndex(e,"center"),setTimeout(()=>{let t=this.listContainer.querySelector(`[data-index="${e}"]`);t&&t.focus()},20)}setupVirtualizedList(){this.listContainer.textContent="",this.listContainer.style.maxHeight=`${this.listHeight}px`,this.virtualizedList=new h.Z(this.listContainer,{height:this.listHeight,rowCount:this.listLength,renderRow:this.renderRow.bind(this),rowHeight:e=>{let t=this.isMobileViewport?54:33;return this.showCreateRow&&e===this.listLength-1?51:t},onRowsRendered:()=>{this.hiddenCurrentElement&&(this.listContainer.removeChild(this.hiddenCurrentElement),delete this.hiddenCurrentElement),this.isCurrentVisible?this.isCurrentVisible=!1:this.hiddenCurrentItemTemplate&&(this.hiddenCurrentElement=document.createElement("div"),this.hiddenCurrentElement?.appendChild(this.renderTemplate(this.hiddenCurrentItemTemplate,{refName:this.currentCommittish})),this.listContainer.appendChild(this.hiddenCurrentElement))},initialIndex:0,overscanCount:6}),this.virtualizedList.resize.bind(this.virtualizedList)}constructor(...e){super(...e),this.isCurrentVisible=!1,this.currentSelectionIndex=null,this.handleWindowResize=()=>{if(!this.virtualizedList)return;let e=this.isMobileViewport,t=this.windowHeight;this.updateViewportSize();let i=e!==this.isMobileViewport,s=t!==this.windowHeight;if(i){this.virtualizedList.destroy(),this.setupVirtualizedList();return}this.isMobileViewport&&s&&(this.listContainer.style.maxHeight=`${this.listHeight}px`,this.virtualizedList.resize(this.listHeight))},this.windowResized=()=>{this.resizeAnimationRequest&&cancelAnimationFrame(this.resizeAnimationRequest),this.resizeAnimationRequest=requestAnimationFrame(this.handleWindowResize)}}};a([n.fA],o.prototype,"listContainer",void 0),a([n.fA],o.prototype,"itemTemplate",void 0),a([n.fA],o.prototype,"noMatchTemplate",void 0),a([n.fA],o.prototype,"fetchFailedTemplate",void 0),a([n.fA],o.prototype,"hiddenCurrentItemTemplate",void 0),o=a([n.Ih],o)},70567:(e,t,i)=>{i.d(t,{W:()=>SearchIndex,r:()=>s});var s,r=i(44544),n=i(71643);let{getItem:h,setItem:a,removeItem:o}=(0,r.Z)("localStorage",{throwQuotaErrorsOnSet:!0});!function(e){e.Branch="branch",e.Tag="tag"}(s||(s={}));let SearchIndex=class SearchIndex{render(){this.selector.render()}async fetchData(){try{if(!this.isLoading||this.fetchInProgress)return;if(!this.bootstrapFromLocalStorage()){this.fetchInProgress=!0,this.fetchFailed=!1;let e=await fetch(`${this.refEndpoint}?type=${this.refType}`,{headers:{Accept:"application/json"}});await this.processResponse(e)}this.isLoading=!1,this.fetchInProgress=!1,this.render()}catch(e){this.fetchInProgress=!1,this.fetchFailed=!0}}async processResponse(e){if(this.emitStats(e),!e.ok){this.fetchFailed=!0;return}let t=e.clone(),i=await e.json();this.knownItems=i.refs,this.cacheKey=i.cacheKey,this.flushToLocalStorage(await t.text())}emitStats(e){if(!e.ok){(0,n.b)({incrementKey:"REF_SELECTOR_BOOT_FAILED"},!0);return}switch(e.status){case 200:(0,n.b)({incrementKey:"REF_SELECTOR_BOOTED_FROM_UNCACHED_HTTP"});break;case 304:(0,n.b)({incrementKey:"REF_SELECTOR_BOOTED_FROM_HTTP_CACHE"});break;default:(0,n.b)({incrementKey:"REF_SELECTOR_UNEXPECTED_RESPONSE"})}}search(e){let t;if(this.searchTerm=e,""===e){this.currentSearchResult=this.knownItems;return}let i=[],s=[];for(let r of(this.exactMatchFound=!1,this.knownItems))if(!((t=r.indexOf(e))<0)){if(0===t){e===r?(s.unshift(r),this.exactMatchFound=!0):s.push(r);continue}i.push(r)}this.currentSearchResult=[...s,...i]}bootstrapFromLocalStorage(){let e=h(this.localStorageKey);if(!e)return!1;let t=JSON.parse(e);return t.cacheKey===this.cacheKey&&"refs"in t?(this.knownItems=t.refs,this.isLoading=!1,(0,n.b)({incrementKey:"REF_SELECTOR_BOOTED_FROM_LOCALSTORAGE"}),!0):(o(this.localStorageKey),!1)}async flushToLocalStorage(e){try{a(this.localStorageKey,e)}catch(t){if(t.message.toLowerCase().includes("quota")){this.clearSiblingLocalStorage(),(0,n.b)({incrementKey:"REF_SELECTOR_LOCALSTORAGE_OVERFLOWED"});try{a(this.localStorageKey,e)}catch(e){e.message.toLowerCase().includes("quota")&&(0,n.b)({incrementKey:"REF_SELECTOR_LOCALSTORAGE_GAVE_UP"})}}else throw t}}clearSiblingLocalStorage(){for(let e of Object.keys(localStorage))e.startsWith(SearchIndex.LocalStoragePrefix)&&o(e)}clearLocalStorage(){o(this.localStorageKey)}get localStorageKey(){return`${SearchIndex.LocalStoragePrefix}:${this.nameWithOwner}:${this.refType}`}constructor(e,t,i,s,r){this.knownItems=[],this.currentSearchResult=[],this.exactMatchFound=!1,this.searchTerm="",this.isLoading=!0,this.fetchInProgress=!1,this.fetchFailed=!1,this.refType=e,this.selector=t,this.refEndpoint=i,this.cacheKey=s,this.nameWithOwner=r}};SearchIndex.LocalStoragePrefix="ref-selector"}}]);
//# sourceMappingURL=app_assets_modules_github_ref-selector_ts-d5fab7fe5db2.js.map