import os
from tailwind_redesign import get_header, get_footer, get_tailwind_head

html = get_tailwind_head("Color Palette Generator", 2) + get_header(2, 'projects') + '''
    <main class="flex-grow w-full h-full flex flex-col pt-12 pb-20">
        
        <div class="text-center mb-8 px-4">
            <h1 class="text-3xl font-extrabold text-primary mb-2">Palette & Contrast Generator</h1>
            <p class="text-secondary text-sm">Press <kbd class="px-2 py-1 bg-gray-200 rounded-md font-mono text-gray-700 font-bold mx-1">Spacebar</kbd> to generate. Click a hex code to copy. Check contrast for accessibility.</p>
        </div>

        <div class="flex-grow flex flex-col md:flex-row w-full max-w-7xl mx-auto px-4 gap-4 h-96 min-h-[500px]" id="palette-container">
            <!-- Colors injected via JS -->
        </div>
        
        <!-- Contrast Checker UI -->
        <div class="max-w-3xl mx-auto w-full mt-12 px-4">
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
                <h3 class="font-bold text-gray-800 text-lg mb-4 flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                    WCAG Accessibility Contrast Checker
                </h3>
                
                <div class="flex flex-col md:flex-row gap-6 items-center">
                    <!-- Dropdowns -->
                    <div class="flex gap-4 w-full md:w-auto">
                        <div class="flex-1">
                            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Text Color</label>
                            <select id="selText" class="w-full bg-gray-50 border border-gray-300 rounded-lg px-3 py-2 text-sm font-medium focus:ring-2 focus:ring-accent outline-none cursor-pointer"></select>
                        </div>
                        <div class="flex-1">
                            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Background</label>
                            <select id="selBg" class="w-full bg-gray-50 border border-gray-300 rounded-lg px-3 py-2 text-sm font-medium focus:ring-2 focus:ring-accent outline-none cursor-pointer"></select>
                        </div>
                    </div>
                    
                    <!-- Result Preview -->
                    <div class="flex-grow flex items-center justify-between bg-gray-50 rounded-xl p-4 border border-gray-200 w-full">
                        <div id="previewBox" class="px-6 py-3 rounded-lg font-bold text-lg border border-black/10 transition-colors shadow-sm">
                            Preview Text
                        </div>
                        <div class="text-right">
                            <div id="ratioText" class="text-2xl font-black text-gray-800 tracking-tight">0.00</div>
                            <div id="wcagBadge" class="text-xs font-bold uppercase px-2 py-1 rounded inline-block mt-1 bg-gray-200 text-gray-600">Checking...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="toast" class="fixed bottom-10 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white px-6 py-3 rounded-full font-medium shadow-xl opacity-0 pointer-events-none transition-opacity duration-300 z-50">
            Copied to clipboard!
        </div>

    </main>

    <script>
        const container = document.getElementById('palette-container');
        const selText = document.getElementById('selText');
        const selBg = document.getElementById('selBg');
        let currentColors = [];

        // Random Hex Generator
        function randHex() {
            return '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
        }

        // Relative Luminance formula for WCAG
        function getLuminance(r, g, b) {
            let a = [r, g, b].map(function (v) {
                v /= 255;
                return v <= 0.03928 ? v / 12.92 : Math.pow( (v + 0.055) / 1.055, 2.4 );
            });
            return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
        }

        function hexToRgb(hex) {
            let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? {
                r: parseInt(result[1], 16),
                g: parseInt(result[2], 16),
                b: parseInt(result[3], 16)
            } : null;
        }

        function getContrastRatio(hex1, hex2) {
            const rgb1 = hexToRgb(hex1);
            const rgb2 = hexToRgb(hex2);
            if(!rgb1 || !rgb2) return 1;
            
            const lum1 = getLuminance(rgb1.r, rgb1.g, rgb1.b);
            const lum2 = getLuminance(rgb2.r, rgb2.g, rgb2.b);
            
            const brightest = Math.max(lum1, lum2);
            const darkest = Math.min(lum1, lum2);
            
            return (brightest + 0.05) / (darkest + 0.05);
        }

        function getTextColor(bgColorHex) {
            const rgb = hexToRgb(bgColorHex);
            if(!rgb) return '#000000';
            const lum = getLuminance(rgb.r, rgb.g, rgb.b);
            return lum > 0.5 ? '#000000' : '#ffffff';
        }

        function copyHex(hex) {
            navigator.clipboard.writeText(hex);
            const toast = document.getElementById('toast');
            toast.textContent = `Copied ${hex}!`;
            toast.classList.remove('opacity-0');
            setTimeout(() => toast.classList.add('opacity-0'), 2000);
        }

        function generatePalette() {
            container.innerHTML = '';
            selText.innerHTML = '';
            selBg.innerHTML = '';
            currentColors = [];
            
            for(let i=0; i<5; i++) {
                const hex = randHex();
                currentColors.push(hex);
                const txtColor = getTextColor(hex);
                
                // Add column
                const col = document.createElement('div');
                col.className = 'flex-1 rounded-2xl md:rounded-3xl flex items-end justify-center pb-6 transition-all duration-300 hover:flex-[1.5] shadow-sm cursor-pointer border border-black/5 group overflow-hidden relative';
                col.style.backgroundColor = hex;
                col.onclick = () => copyHex(hex);
                
                col.innerHTML = `
                    <div class="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-colors"></div>
                    <div class="relative z-10 bg-white/20 backdrop-blur-md px-4 py-2 rounded-xl text-center transform translate-y-4 group-hover:translate-y-0 opacity-0 group-hover:opacity-100 transition-all border border-white/20">
                        <div class="font-bold text-lg font-mono tracking-wider" style="color: ${txtColor}">${hex.toUpperCase()}</div>
                        <div class="text-xs font-medium opacity-80" style="color: ${txtColor}">Click to copy</div>
                    </div>
                `;
                container.appendChild(col);
                
                // Add to dropdowns
                selText.innerHTML += `<option value="${hex}">Color ${i+1} (${hex})</option>`;
                selBg.innerHTML += `<option value="${hex}">Color ${i+1} (${hex})</option>`;
            }
            
            // Set defaults for checker
            selText.selectedIndex = 0;
            selBg.selectedIndex = 1;
            checkContrast();
        }

        function checkContrast() {
            const tHex = selText.value;
            const bHex = selBg.value;
            
            const ratio = getContrastRatio(tHex, bHex);
            const ratioFormatted = ratio.toFixed(2);
            
            const preview = document.getElementById('previewBox');
            preview.style.color = tHex;
            preview.style.backgroundColor = bHex;
            
            const rText = document.getElementById('ratioText');
            rText.textContent = ratioFormatted + ':1';
            
            const badge = document.getElementById('wcagBadge');
            
            if(ratio >= 7) {
                badge.textContent = 'AAA (Excellent)';
                badge.className = 'text-xs font-bold uppercase px-2 py-1 rounded inline-block mt-1 bg-emerald-100 text-emerald-700';
            } else if(ratio >= 4.5) {
                badge.textContent = 'AA (Good)';
                badge.className = 'text-xs font-bold uppercase px-2 py-1 rounded inline-block mt-1 bg-blue-100 text-blue-700';
            } else if(ratio >= 3) {
                badge.textContent = 'AA Large Text Only';
                badge.className = 'text-xs font-bold uppercase px-2 py-1 rounded inline-block mt-1 bg-amber-100 text-amber-700';
            } else {
                badge.textContent = 'Fail (Poor)';
                badge.className = 'text-xs font-bold uppercase px-2 py-1 rounded inline-block mt-1 bg-red-100 text-red-700';
            }
        }

        selText.addEventListener('change', checkContrast);
        selBg.addEventListener('change', checkContrast);
        
        document.addEventListener('keydown', (e) => {
            if(e.code === 'Space') {
                e.preventDefault();
                generatePalette();
            }
        });

        // Initial run
        generatePalette();
    </script>
''' + get_footer(2)

os.makedirs('./projects/color-palette', exist_ok=True)
with open('./projects/color-palette/index.html', 'w') as f:
    f.write(html)

print("Generated Color Palette App")
