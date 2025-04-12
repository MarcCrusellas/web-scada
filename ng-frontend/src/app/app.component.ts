import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <h1>{{ title }}</h1>
    <nav>
      <a routerLink="/screens">Screen List</a> |
      <a routerLink="/library">Library Creator</a>
    </nav>
    <router-outlet></router-outlet>
  `,
  imports: [RouterModule]
})
export class AppComponent {
  title = 'SCADA Dashboard';
}
