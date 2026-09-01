import os
from tailwind_redesign import get_header, get_footer, get_tailwind_head

html = get_tailwind_head("Pomodoro Timer & Focus Room", 2) + get_header(2, 'projects') + '''
    <main class="flex-grow flex items-center justify-center py-12 px-4 w-full bg-gray-50 transition-colors duration-500" id="app-bg">
        <div class="max-w-md w-full bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
            <!-- Header -->
            <div class="p-6 text-center border-b border-gray-100">
                <h1 class="text-2xl font-bold text-gray-800 flex justify-center items-center gap-2">
                    <svg class="w-6 h-6 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/></svg>
                    Focus Room
                </h1>
                <p class="text-sm text-gray-500 mt-1">Boost your productivity with timed sessions.</p>
            </div>

            <!-- Mode Selector -->
            <div class="flex justify-center p-6 gap-3">
                <button id="mode-pomodoro" class="mode-btn px-4 py-2 rounded-full text-sm font-bold bg-red-100 text-red-700 transition-all">Pomodoro</button>
                <button id="mode-short" class="mode-btn px-4 py-2 rounded-full text-sm font-bold text-gray-500 hover:bg-gray-100 transition-all">Short Break</button>
                <button id="mode-long" class="mode-btn px-4 py-2 rounded-full text-sm font-bold text-gray-500 hover:bg-gray-100 transition-all">Long Break</button>
            </div>

            <!-- Timer Display -->
            <div class="py-10 text-center">
                <div id="time-display" class="text-7xl font-black text-gray-800 tracking-tight tabular-nums">25:00</div>
                <div id="status-text" class="text-gray-400 font-medium mt-2 uppercase tracking-widest text-sm">Time to Focus</div>
            </div>

            <!-- Controls -->
            <div class="flex justify-center gap-4 pb-10">
                <button id="start-btn" class="w-20 h-20 rounded-full bg-red-500 text-white flex items-center justify-center hover:bg-red-600 hover:scale-105 transition-all shadow-lg shadow-red-200">
                    <svg class="w-8 h-8 ml-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/></svg>
                </button>
                <button id="pause-btn" class="hidden w-20 h-20 rounded-full bg-gray-800 text-white flex items-center justify-center hover:bg-gray-900 hover:scale-105 transition-all shadow-lg">
                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                </button>
                <button id="reset-btn" class="w-14 h-14 rounded-full bg-gray-100 text-gray-600 flex items-center justify-center hover:bg-gray-200 transition-all self-center ml-2">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                </button>
            </div>

            <!-- Stats Footer -->
            <div class="bg-gray-50 p-4 text-center border-t border-gray-100 flex justify-around">
                <div>
                    <div class="text-xs text-gray-400 font-bold uppercase">Sessions</div>
                    <div id="session-count" class="text-lg font-black text-gray-700">0</div>
                </div>
            </div>
        </div>
    </main>

    <script>
        const MODES = {
            pomodoro: { time: 25 * 60, color: 'bg-red-500', bg: 'bg-red-50', text: 'Time to Focus', btnColor: 'bg-red-100 text-red-700' },
            short: { time: 5 * 60, color: 'bg-teal-500', bg: 'bg-teal-50', text: 'Take a Break', btnColor: 'bg-teal-100 text-teal-700' },
            long: { time: 15 * 60, color: 'bg-blue-500', bg: 'bg-blue-50', text: 'Long Break', btnColor: 'bg-blue-100 text-blue-700' }
        };

        let currentMode = 'pomodoro';
        let timeLeft = MODES[currentMode].time;
        let timer = null;
        let sessions = 0;

        const timeDisplay = document.getElementById('time-display');
        const statusText = document.getElementById('status-text');
        const startBtn = document.getElementById('start-btn');
        const pauseBtn = document.getElementById('pause-btn');
        const resetBtn = document.getElementById('reset-btn');
        const appBg = document.getElementById('app-bg');
        const sessionCount = document.getElementById('session-count');

        const modeBtns = {
            pomodoro: document.getElementById('mode-pomodoro'),
            short: document.getElementById('mode-short'),
            long: document.getElementById('mode-long')
        };

        function updateDisplay() {
            const minutes = Math.floor(timeLeft / 60).toString().padStart(2, '0');
            const seconds = (timeLeft % 60).toString().padStart(2, '0');
            timeDisplay.textContent = `${minutes}:${seconds}`;
            document.title = `${minutes}:${seconds} - Focus Room`;
        }

        function setMode(mode) {
            clearInterval(timer);
            timer = null;
            currentMode = mode;
            timeLeft = MODES[mode].time;
            statusText.textContent = MODES[mode].text;
            
            // Update UI colors
            appBg.className = `flex-grow flex items-center justify-center py-12 px-4 w-full transition-colors duration-500 ${MODES[mode].bg}`;
            startBtn.className = `w-20 h-20 rounded-full text-white flex items-center justify-center hover:scale-105 transition-all shadow-lg ${MODES[mode].color} hover:opacity-90`;
            
            // Update mode buttons
            Object.keys(modeBtns).forEach(k => {
                modeBtns[k].className = 'mode-btn px-4 py-2 rounded-full text-sm font-bold text-gray-500 hover:bg-gray-100 transition-all';
            });
            modeBtns[mode].className = `mode-btn px-4 py-2 rounded-full text-sm font-bold transition-all ${MODES[mode].btnColor}`;
            
            startBtn.classList.remove('hidden');
            pauseBtn.classList.add('hidden');
            updateDisplay();
        }

        function startTimer() {
            if (timer) return;
            // Request notification permission
            if (Notification.permission !== "granted") Notification.requestPermission();
            
            startBtn.classList.add('hidden');
            pauseBtn.classList.remove('hidden');
            
            timer = setInterval(() => {
                timeLeft--;
                updateDisplay();
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    timer = null;
                    if (currentMode === 'pomodoro') {
                        sessions++;
                        sessionCount.textContent = sessions;
                    }
                    if (Notification.permission === "granted") {
                        new Notification("Time's up!", { body: currentMode === 'pomodoro' ? "Time for a break!" : "Back to work!" });
                    }
                    // Auto switch modes
                    if (currentMode === 'pomodoro') {
                        setMode(sessions % 4 === 0 ? 'long' : 'short');
                    } else {
                        setMode('pomodoro');
                    }
                }
            }, 1000);
        }

        function pauseTimer() {
            clearInterval(timer);
            timer = null;
            pauseBtn.classList.add('hidden');
            startBtn.classList.remove('hidden');
        }

        function resetTimer() {
            setMode(currentMode);
        }

        modeBtns.pomodoro.addEventListener('click', () => setMode('pomodoro'));
        modeBtns.short.addEventListener('click', () => setMode('short'));
        modeBtns.long.addEventListener('click', () => setMode('long'));
        startBtn.addEventListener('click', startTimer);
        pauseBtn.addEventListener('click', pauseTimer);
        resetBtn.addEventListener('click', resetTimer);

        updateDisplay();
    </script>
''' + get_footer(2)

os.makedirs('./projects/pomodoro-timer', exist_ok=True)
with open('./projects/pomodoro-timer/index.html', 'w') as f:
    f.write(html)

print("Generated Pomodoro Timer")
