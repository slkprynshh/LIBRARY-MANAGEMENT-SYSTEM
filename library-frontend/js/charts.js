async function initAdminCharts() {
  const barCtx = document.getElementById('barChart');
  const pieCtx = document.getElementById('pieChart');
  if (!barCtx || !pieCtx) return;

  let monthlyLabels = MOCK.chartData.monthly.labels;
  let monthlyData = MOCK.chartData.monthly.data;
  let genreLabels = MOCK.chartData.categories.labels;
  let genreData = MOCK.chartData.categories.data;

  if (typeof api !== 'undefined') {
    const mRes = await api.getMonthlyIssues();
    if (mRes && mRes.success && mRes.data && mRes.data.monthly_issues.length > 0) {
      const monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      monthlyLabels = mRes.data.monthly_issues.map(m => monthNames[(m.month - 1) % 12]);
      monthlyData = mRes.data.monthly_issues.map(m => m.count);
    }

    const gRes = await api.getGenreDistribution();
    if (gRes && gRes.success && gRes.data && gRes.data.genre_distribution.length > 0) {
      genreLabels = gRes.data.genre_distribution.map(g => g.genre);
      genreData = gRes.data.genre_distribution.map(g => g.count);
    }
  }

  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: monthlyLabels,
      datasets: [{
        label: 'Books Issued',
        data: monthlyData,
        backgroundColor: 'rgba(14,165,233,0.7)',
        borderColor: '#0EA5E9',
        borderWidth: 2,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
        x: { grid: { display: false } }
      }
    }
  });

  new Chart(pieCtx, {
    type: 'doughnut',
    data: {
      labels: genreLabels,
      datasets: [{
        data: genreData,
        backgroundColor: ['#0EA5E9','#10B981','#F59E0B','#EF4444','#8B5CF6','#6B7280','#EC4899','#14B8A6'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { padding: 16, font: { size: 12 } } }
      },
      cutout: '60%'
    }
  });
}
