import { Routes } from '@angular/router';
import { ScreensComponent } from './screens/screens.component';
import { LibraryComponent } from './library/library.component';

export const routes: Routes = [
  { path: 'screens', component: ScreensComponent },
  { path: 'library', component: LibraryComponent },
  { path: '', redirectTo: '/screens', pathMatch: 'full' }
];
