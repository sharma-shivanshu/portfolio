import os
from tailwind_redesign import get_header, get_footer, get_tailwind_head

html = get_tailwind_head("The Breathing Room", 2) + '''
    <style>
        /* Box Breathing Animation */
        @keyframes boxBreathe {
            0% { transform: scale(1); background-color: #38bdf8; } /* Start Inhale (grow) */
            25% { transform: scale(2.5); background-color: #818cf8; } /* End Inhale / Start Hold */
            50% { transform: scale(2.5); background-color: #c084fc; } /* End Hold / Start Exhale (shrink) */
            75% { transform: scale(1); background-color: #f472b6; } /* End Exhale / Start Hold */
            100% { transform: scale(1); background-color: #38bdf8; } /* End Hold / Loop */
        }
        
        @keyframes textBreathe {
            0% { content: "Inhale"; opacity: 1; }
            22% { opacity: 0; }
            25% { content: "Hold"; opacity: 1; }
            47% { opacity: 0; }
            50% { content: "Exhale"; opacity: 1; }
            72% { opacity: 0; }
            75% { content: "Hold"; opacity: 1; }
            97% { opacity: 0; }
            100% { content: "Inhale"; opacity: 1; }
        }

        .animate-breathe {
            animation: boxBreathe 16s ease-in-out infinite;
        }
        
        .breathe-text::after {
            content: "Inhale";
            animation: textBreathe 16s ease-in-out infinite;
        }
        
        /* Pause state */
        .paused .animate-breathe, .paused .breathe-text::after {
            animation-play-state: paused;
        }
        .paused-text { display: none; }
        .paused .paused-text { display: block; }
        .paused .breathe-text { display: none; }
    </style>
''' + get_header(2, 'projects') + '''
    <main class="flex-grow w-full flex flex-col bg-gray-900 min-h-screen relative overflow-hidden transition-colors duration-1000" id="mainBg">
        
        <!-- Subtle background glowing orbs -->
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style="animation-delay: 2s;"></div>

        <div class="relative z-10 flex flex-col items-center justify-center flex-grow py-20 px-4 h-full">
            
            <div class="text-center mb-16">
                <h1 class="text-3xl font-bold text-white mb-2 tracking-wide">The Breathing Room</h1>
                <p class="text-gray-400 text-sm max-w-md mx-auto">Follow the circle to practice Box Breathing. Inhale for 4s, Hold for 4s, Exhale for 4s, Hold for 4s.</p>
            </div>

            <!-- Breathing Circle -->
            <div class="relative w-64 h-64 flex items-center justify-center mb-16" id="breatheWrapper">
                <!-- Guide Ring -->
                <div class="absolute w-full h-full rounded-full border-2 border-gray-700 opacity-50"></div>
                <div class="absolute w-[250%] h-[250%] rounded-full border-2 border-gray-700 opacity-20 border-dashed"></div>
                
                <!-- Animated Circle -->
                <div class="w-24 h-24 rounded-full bg-sky-400 opacity-80 animate-breathe shadow-[0_0_40px_rgba(56,189,248,0.5)]"></div>
                
                <!-- Text Overlay -->
                <div class="absolute text-white font-bold tracking-widest text-xl drop-shadow-lg z-20">
                    <span class="breathe-text"></span>
                    <span class="paused-text tracking-normal">Paused</span>
                </div>
            </div>

            <!-- Controls -->
            <div class="flex gap-4">
                <button id="toggleBtn" class="w-16 h-16 rounded-full bg-white text-gray-900 flex items-center justify-center hover:bg-gray-200 transition-all shadow-lg hover:scale-105">
                    <svg id="pauseIcon" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                    <svg id="playIcon" class="w-6 h-6 hidden ml-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/></svg>
                </button>
            </div>
            
        </div>
    </main>

    <script>
        const wrapper = document.getElementById('breatheWrapper');
        const btn = document.getElementById('toggleBtn');
        const playIcon = document.getElementById('playIcon');
        const pauseIcon = document.getElementById('pauseIcon');
        
        let isPlaying = true;

        btn.addEventListener('click', () => {
            if(isPlaying) {
                wrapper.classList.add('paused');
                playIcon.classList.remove('hidden');
                pauseIcon.classList.add('hidden');
            } else {
                wrapper.classList.remove('paused');
                playIcon.classList.add('hidden');
                pauseIcon.classList.remove('hidden');
            }
            isPlaying = !isPlaying;
        });
    </script>
''' + get_footer(2)

os.makedirs('./projects/breathing-room', exist_ok=True)
with open('./projects/breathing-room/index.html', 'w') as f:
    f.write(html)

print("Generated Breathing Room App")
