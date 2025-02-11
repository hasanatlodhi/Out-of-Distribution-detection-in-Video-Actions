// change navbar when scrolls 

window.addEventListener('scroll', ()=> 
{
    document.querySelector('nav').classList.toggle
    ('window-scroll', window.scrollY > 0)
} );



//show hide faqs questions

const faqs=document.querySelectorAll('.faq');
faqs.forEach(faq=> {
    faq.addEventListener('click',()=>{
        faq.classList.toggle('open');

        //change icons on click

        const icon=faq.querySelector('.faq_icon i');
        if(icon.className=='uil uil-plus')
        {
            icon.className="uil uil-minus"
        }
        else
        {
            icon.className="uil uil-plus"
        }
    })    
});


//make menu items active

let links = document.querySelectorAll(".nav_menu li a");
let bodyId = document.querySelector("body").id;

for(let link of links){
    if(link.dataset.active == bodyId){
        link.classList.add("active");
    }
}
// login active 
let loginlink = document.querySelector(".loglink li a");
let logbodyId = document.querySelector("body").id;
if(logbodyId=="login")
{
    classList.add("active");
}


//show hide nav menucon
const menu=document.querySelector(".nav_menu")
const menuBtn=document.querySelector(".open_menu_btn")
const closeBtn=document.querySelector(".close_menu_btn")

menuBtn.addEventListener('click',()=>
{
    menu.style.display="flex";
    closeBtn.style.display="inline-block";
    menuBtn.style.display="none";
})

//close nav menu 
const closeNav=()=>{
    menu.style.display="none";
    closeBtn.style.display="none";
    menuBtn.style.display="inline-block";
}

closeBtn.addEventListener('click',closeNav)

/* scroll bar indicator */
const indicator = document.querySelector(".scroll-indicator")    

const scroll = () => {
  const height = document.documentElement.offsetHeight
  const mx = document.documentElement.scrollHeight - document.documentElement.clientHeight
  const perc = document.documentElement.scrollTop * 100  / mx
  indicator.style.width = perc + "%"
}

document.addEventListener("scroll", scroll)      

//show hide header buttons
const main=document.querySelector(".Mainbuttons")
const opnmainBtn=document.querySelector(".open_btn")
const closemainBtn=document.querySelector(".close_btn")

opnmainBtn.addEventListener('click',()=>
{
    main.style.display="flex";
    closemainBtn.style.display="inline-block";
    opnmainBtn.style.display="none";
})

//close nav menu 
const closemabtn=()=>{
    main.style.display="none";
    closemainBtn.style.display="none";
    opnmainBtn.style.display="inline-block";
}

closemainBtn.addEventListener('click',closemabtn)

// popup login 
document.querySelector("#show-login").addEventListener('click',function()
{
    document.querySelector(".main").classList.add("active");
});
document.querySelector(".wrapper .close-btn").addEventListener('click',function()
{
    document.querySelector(".wrapper").classList.remove("active");
});