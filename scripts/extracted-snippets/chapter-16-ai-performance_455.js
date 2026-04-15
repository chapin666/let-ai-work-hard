# Source: chapter-16-ai-performance.md
# Lines: 455-527
# Language: javascript

// 大数据模式配置
const largeDataConfig = {
  // 启用大数据模式
  large: true,
  largeThreshold: 500,
  
  // 降低渲染精度
  progressive: 500,
  progressiveThreshold: 1000,
  
  // 禁用动画
  animation: false,
  
  // 采样（当数据超过阈值时）
  sampling: 'lttb', // Largest Triangle Three Bucket
  
  // 禁用一些耗时的特效
  showSymbol: false,
  hoverAnimation: false,
  
  // 减少tooltip的复杂度
  tooltip: {
    show: true,
    trigger: 'axis',
    // 使用简单的formatter
    formatter: '{b}: {c}'
  }
};

// 折线图优化
const lineChartOption = {
  series: [{
    type: 'line',
    data: largeDataSet,
    ...largeDataConfig,
    // 数据分组，减少渲染压力
    dimensions: ['time', 'value'],
    encode: {
      x: 'time',
      y: 'value'
    }
  }]
};

// 懒加载非首屏图表
const chartRef = useRef(null);
const [isVisible, setIsVisible] = useState(false);

useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true);
        observer.disconnect();
      }
    },
    { threshold: 0.1 }
  );
  
  if (chartRef.current) {
    observer.observe(chartRef.current);
  }
  
  return () => observer.disconnect();
}, []);

return (
  <div ref={chartRef}>
    {isVisible && <ECharts option={lineChartOption} />}
  </div>
);
