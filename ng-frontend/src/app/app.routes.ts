import { Routes } from '@angular/router';
import { ScreensComponent } from './screens/screens.component';
import { LibraryComponent } from './library/library.component';
import { TestCommunicationComponent } from './test-communication/test-communication.component';

export const routes: Routes = [
  { path: 'screens', component: ScreensComponent },
  { path: 'library', component: LibraryComponent },
  { path: 'test-communication', component: TestCommunicationComponent },
  { path: '', redirectTo: '/screens', pathMatch: 'full' }
];
