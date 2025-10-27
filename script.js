// (() => {
//     const input1=document.getElementById('input1');
//     const input2=document.getElementById('input2');
//     const searchBtn=document.getElementById('searchBtn');
//     const generateBtn=document.getElementById('generateBtn');
//     const profileArea=document.getElementById('profileArea');
//     const status=document.getElementById('status');
//     const compareToggle=document.getElementById('compareToggle');
//     const repoList=document.getElementById('repoList');
//     const settingBtn=document.getElementById('settingBtn');
//     const settingsModal=document.getElementById('settingsModal');
//     const saveSettings=document.getElementById('saveSettings');
//     const closeSettings=document.getElementById('closeSettings');
//     const trendingList=document.getElementById('trendingList');
//     const tokenInput=document.getElementById('tokenInput');
//     const collabList=document.getElementById('collabList');
//     const langCtx=document.getElementById('langCtx').getContext('2d');
//     const starCtx=document.getElementById('starCtx').getContext('2d');
//     const userCardT=document.getElementById('userCardT');
//     let langChart,starChart;

//     async function fetchUserAndRepos(username){
//         const [user,repos]=await Promise.all([
//             ghFetch(`https://api.github.com/users/${encodeURIComponent(username)}`),
//             ghFetch(`https://api.github.com/users/${encodeURIComponent(username)}/repos?type=owner&sort=updated&per_page=100`)
//         ]);
//         return {user,repos};
//     }
//     })();




    gsap.from(".title", {
        duration: 1,
        y: -40,
        opacity: 0,
        ease: "power3.out"
    });
    gsap.from(".controls", {
        duration: 1,
        x: 40,
        opacity: 0,
        delay: 0.3,
        ease: "power3.out"
    });
    gsap.from(".searchSection", {
        duration: 1,
        y: 40,
        opacity: 0,
        delay: 0.6,
        ease: "power3.out"
    });
    gsap.from([".profileArea", ".chartCard"], {
        duration: 1,
        opacity: 0,
        y: 50,
        delay: 1,
        stagger: 0.3,
        ease: "power3.out"
    });
    gsap.from(".repoList", {
        duration: 0.8,
        opacity: 0,
        scale: 0.9,
        stagger: 0.1,
        delay: 1.5,
        ease: "back.out(1.7)"
    });
    




