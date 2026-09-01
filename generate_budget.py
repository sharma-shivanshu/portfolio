import os
from tailwind_redesign import get_header, get_footer, get_tailwind_head

html = get_tailwind_head("Personal Finance Visualizer", 2) + get_header(2, 'projects') + '''
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <main class="flex-grow max-w-6xl mx-auto px-4 sm:px-6 py-12 w-full">
        <div class="text-center mb-10">
            <h1 class="text-3xl font-extrabold text-primary mb-2">Personal Budget Visualizer</h1>
            <p class="text-secondary">Input your income and expenses to instantly map your cash flow.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left: Inputs -->
            <div class="space-y-6">
                <!-- Income -->
                <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
                    <h2 class="text-lg font-bold text-emerald-600 mb-4 flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Monthly Income
                    </h2>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <span class="text-gray-500 sm:text-sm">₹</span>
                        </div>
                        <input type="number" id="incomeInput" value="50000" class="w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 font-bold text-gray-700 text-lg" placeholder="0.00">
                    </div>
                </div>

                <!-- Expenses -->
                <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
                    <h2 class="text-lg font-bold text-red-500 mb-4 flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Monthly Expenses
                    </h2>
                    
                    <form id="expenseForm" class="flex gap-2 mb-6">
                        <input type="text" id="expName" required class="flex-grow bg-gray-50 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-red-400" placeholder="e.g. Rent">
                        <input type="number" id="expAmount" required class="w-32 bg-gray-50 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-red-400" placeholder="₹ Amount">
                        <button type="submit" class="bg-red-500 hover:bg-red-600 text-white px-4 rounded-lg font-bold transition-colors">+</button>
                    </form>

                    <div class="max-h-64 overflow-y-auto pr-2" id="expenseList">
                        <!-- Expenses injected here -->
                    </div>
                </div>
            </div>

            <!-- Right: Chart & Summary -->
            <div class="space-y-6">
                <!-- Summary Cards -->
                <div class="grid grid-cols-3 gap-4">
                    <div class="bg-emerald-50 border border-emerald-100 rounded-xl p-4 text-center">
                        <div class="text-xs font-bold text-emerald-600 uppercase tracking-wide mb-1">Total Income</div>
                        <div id="sumIncome" class="text-xl font-black text-emerald-700">₹0</div>
                    </div>
                    <div class="bg-red-50 border border-red-100 rounded-xl p-4 text-center">
                        <div class="text-xs font-bold text-red-600 uppercase tracking-wide mb-1">Total Expenses</div>
                        <div id="sumExpenses" class="text-xl font-black text-red-700">₹0</div>
                    </div>
                    <div class="bg-blue-50 border border-blue-100 rounded-xl p-4 text-center">
                        <div class="text-xs font-bold text-blue-600 uppercase tracking-wide mb-1">Remaining</div>
                        <div id="sumBalance" class="text-xl font-black text-blue-700">₹0</div>
                    </div>
                </div>

                <!-- Chart -->
                <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-200 flex flex-col items-center">
                    <h2 class="text-lg font-bold text-primary mb-4 self-start">Expense Breakdown</h2>
                    <div class="relative w-full h-72 flex justify-center">
                        <canvas id="budgetChart"></canvas>
                        <div id="chartCenter" class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none mt-4">
                            <span class="text-sm font-bold text-gray-400">Savings Rate</span>
                            <span id="savingsRate" class="text-2xl font-black text-emerald-500">0%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        // State
        let income = 50000;
        let expenses = [
            { id: 1, name: 'Rent', amount: 15000 },
            { id: 2, name: 'Groceries', amount: 8000 },
            { id: 3, name: 'Utilities', amount: 3000 },
            { id: 4, name: 'Entertainment', amount: 4000 }
        ];
        let chartInstance = null;
        
        // Colors for chart
        const colors = ['#f87171', '#fb923c', '#fbbf24', '#a3e635', '#34d399', '#22d3ee', '#818cf8', '#c084fc', '#f472b6'];

        // Elements
        const incomeInput = document.getElementById('incomeInput');
        const expenseForm = document.getElementById('expenseForm');
        const expName = document.getElementById('expName');
        const expAmount = document.getElementById('expAmount');
        const expenseList = document.getElementById('expenseList');
        
        const sumIncome = document.getElementById('sumIncome');
        const sumExpenses = document.getElementById('sumExpenses');
        const sumBalance = document.getElementById('sumBalance');
        const savingsRate = document.getElementById('savingsRate');

        // Events
        incomeInput.addEventListener('input', (e) => {
            income = parseFloat(e.target.value) || 0;
            updateUI();
        });

        expenseForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = expName.value.trim();
            const amount = parseFloat(expAmount.value);
            if (name && amount > 0) {
                expenses.push({ id: Date.now(), name, amount });
                expName.value = '';
                expAmount.value = '';
                updateUI();
            }
        });

        function deleteExpense(id) {
            expenses = expenses.filter(e => e.id !== id);
            updateUI();
        }

        // Logic
        function updateUI() {
            // Render List
            expenseList.innerHTML = '';
            let totalExp = 0;
            
            expenses.forEach((exp, idx) => {
                totalExp += exp.amount;
                const color = colors[idx % colors.length];
                expenseList.innerHTML += `
                    <div class="flex justify-between items-center py-3 border-b border-gray-100 last:border-0 group">
                        <div class="flex items-center">
                            <div class="w-3 h-3 rounded-full mr-3" style="background-color: ${color}"></div>
                            <span class="font-medium text-gray-700">${exp.name}</span>
                        </div>
                        <div class="flex items-center gap-4">
                            <span class="font-bold text-gray-900">₹${exp.amount.toLocaleString('en-IN')}</span>
                            <button onclick="deleteExpense(${exp.id})" class="text-red-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                            </button>
                        </div>
                    </div>
                `;
            });

            // Update Summary
            const balance = income - totalExp;
            const rate = income > 0 ? Math.max(0, (balance / income) * 100) : 0;
            
            sumIncome.textContent = '₹' + income.toLocaleString('en-IN');
            sumExpenses.textContent = '₹' + totalExp.toLocaleString('en-IN');
            sumBalance.textContent = '₹' + balance.toLocaleString('en-IN');
            savingsRate.textContent = rate.toFixed(1) + '%';
            
            sumBalance.className = `text-xl font-black ${balance >= 0 ? 'text-blue-700' : 'text-red-600'}`;

            // Draw Chart
            drawChart(totalExp, balance);
        }

        function drawChart(totalExp, balance) {
            if (chartInstance) chartInstance.destroy();
            
            const labels = expenses.map(e => e.name);
            const data = expenses.map(e => e.amount);
            const bgColors = expenses.map((_, i) => colors[i % colors.length]);

            // If there's savings, show it on the chart
            if (balance > 0) {
                labels.push('Savings');
                data.push(balance);
                bgColors.push('#f3f4f6'); // gray for savings
            }

            const ctx = document.getElementById('budgetChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: bgColors,
                        borderWidth: 0,
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: {
                        legend: { position: 'right', labels: { font: { family: 'Inter' } } }
                    }
                }
            });
        }

        // Init
        updateUI();
    </script>
''' + get_footer(2)

os.makedirs('./projects/budget-visualizer', exist_ok=True)
with open('./projects/budget-visualizer/index.html', 'w') as f:
    f.write(html)

print("Generated Budget Visualizer")
