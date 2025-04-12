import { Component, OnInit, OnDestroy } from '@angular/core';
import { StorageService } from '../../core/services/storage.service';
import {MonacoEditorModule}  from 'ngx-monaco-editor-v2';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css'],
  imports: [MonacoEditorModule, FormsModule],
})
export class CodeEditorComponent implements OnInit, OnDestroy {
  code: string = ''; // Code content to be edited
  private updateTimeout: any = null; // Store the timeout ID

  constructor(private readonly storageService: StorageService) {}

  ngOnInit(): void {
    (window as any).MonacoEnvironment = {
      getWorkerUrl: function (moduleId: string, label: string) {
        return './assets/monaco/min/vs/base/worker/workerMain.js';
      }
    };

    this.storageService.fetchState('code-editor').then((value) => {
      if (value) {
        this.code = value;
      }
    });
  }

  onCodeChange(newCode: string): void {
    this.code = newCode;

    // Clear the previous timeout if it exists
    if (this.updateTimeout) {
      clearTimeout(this.updateTimeout);
    }

    // Set a new timeout to delay sending updates to the backend
    this.updateTimeout = setTimeout(() => {
      this.storageService.updateState('code-editor', this.code); // Send updated code to the server
      this.updateTimeout = null; // Reset the timeout ID after execution
    }, 500); // 500ms delay
  }

  ngOnDestroy(): void {
    // If the component is destroyed, send the update immediately
    if (this.updateTimeout) {
      clearTimeout(this.updateTimeout);
      this.storageService.updateState('code-editor', this.code);
    }
  }
}
