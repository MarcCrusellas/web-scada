import { Component } from '@angular/core';

@Component({
  selector: 'app-library',
  templateUrl: './library.component.html',
//   styleUrls: ['./library.component.css'],
})
export class LibraryComponent {
  libraries = [
    { id: 1, name: 'Library 1' },
    { id: 2, name: 'Library 2' }
  ];

  createLibrary() {
    console.log('Create a new library');
  }

  editLibrary(library: any) {
    console.log('Edit library:', library);
  }
}
