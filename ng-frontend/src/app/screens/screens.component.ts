import { Component } from '@angular/core';
import { StorageService } from '../core/services/storage.service';
import * as uuid from 'uuid';

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
        // this.storageService.fetchState('screens').then((screens) => {
        //     this.screens = screens || [];
        //     console.log('Screens loaded:', this.screens);

        // });
        this.storageService.Communicate({
            type: 'json-key',
            args: {
                env: 'screens',
                type: 'fetch',
                key: 'screens',
            },
            uuid: uuid.v4(),
        }).then((screens) => {
            this.screens = screens || [];
            console.log('Screens loaded:', this.screens);
        });
    }

    createScreen(): void {
        const newScreen = { id: Date.now(), name: `Screen ${this.screens.length + 1}` };
        this.screens.push(newScreen);
        // this.storageService.updateState('screens', this.screens);+
        this.storageService.Communicate({
            type: 'json-key',
            args: {
                env: 'screens',
                type: 'update',
                key: 'screens',
                value: JSON.stringify(this.screens),
            },
            uuid: uuid.v4(),
        });
    }

    editScreen(screen: any): void {
        console.log('Edit screen:', screen);
    }
}
