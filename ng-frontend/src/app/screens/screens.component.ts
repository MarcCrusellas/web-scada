import { Component } from '@angular/core';
import { StorageService } from '../core/services/storage.service';

@Component({
    selector: 'app-screens',
    templateUrl: './screens.component.html',
    // imports: [StorageService],

})
export class ScreensComponent {
    screens: any[] = [];

    constructor(private storageService: StorageService) {
        this.loadScreens();
    }

    loadScreens(): void {
        this.storageService.fetchState('screens').then((screens) => {
            this.screens = screens || [];
            console.log('Screens loaded:', this.screens);
            
        });
    }

    createScreen(): void {
        const newScreen = { id: Date.now(), name: `Screen ${this.screens.length + 1}` };
        this.screens.push(newScreen);
        this.storageService.updateState('screens', this.screens);
    }

    editScreen(screen: any): void {
        console.log('Edit screen:', screen);
    }
}
