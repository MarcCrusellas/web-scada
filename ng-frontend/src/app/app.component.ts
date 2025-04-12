import { Component, AfterViewInit } from '@angular/core';
import * as echarts from 'echarts';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
  private chart: any;
  private data: number[] = [];

  ngAfterViewInit(): void {
    this.initChart();
    this.connectWebSocket();
  }

  private initChart(): void {
    const chartDom = document.getElementById('chart') as HTMLElement;
    if (chartDom) {
      this.chart = echarts.init(chartDom);
      this.chart.setOption({
        xAxis: { type: 'category', data: Array.from({ length: 10 }, (_, i) => i + 1) },
        yAxis: { type: 'value' },
        series: [{ data: this.data, type: 'line' }]
      });
    } else {
      console.error('Chart DOM element not found');
    }
  }

  private connectWebSocket(): void {
    const socket = new WebSocket('ws://localhost:8080');

    socket.onmessage = (event) => {
      const message = event.data;
      console.log('Received message:', message);
      if (message.startsWith('data:')) {
        const value = parseInt(message.replace('data:', ''), 10);
        this.updateChart(value);
      }
    };
  }

  private updateChart(value: number): void {
    this.data.push(value);
    if (this.data.length > 10) {
      this.data.shift();
    }
    this.chart.setOption({
      series: [{ data: this.data, type: 'line' }]
    });
  }
}
