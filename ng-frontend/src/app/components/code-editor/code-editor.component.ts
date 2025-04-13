import { Component, OnInit, OnDestroy } from '@angular/core';
import { StorageService } from '../../core/services/storage.service';
import {MonacoEditorModule}  from 'ngx-monaco-editor-v2';
import { FormsModule } from '@angular/forms';
import * as uuid from 'uuid';

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

    // this.storageService.fetchState('code-editor').then((value) => {
    //   if (value) {
    //     this.code = value;
    //   }
    // });
    this.storageService.Communicate({
      type: 'json-key',
      args: {
        env: 'code-editor',
        type: 'fetch',
        key: 'code-editor',
      },
      uuid: uuid.v4(),
    }).then((value) => {
      if (value) {
        this.code = value;
      }
    });
  }

  onCodeChange(newCode: string): void {
    this.code = newCode;

    if (this.updateTimeout) {
      clearTimeout(this.updateTimeout);
    }

    this.updateTimeout = setTimeout(() => {
      // this.storageService.updateState('code-editor', this.code);
      this.storageService.Communicate({
        type: 'json-key',
        args: {
          env: 'code-editor',
          type: 'update',
          key: 'code-editor',
          value: this.code,
        },
        uuid: uuid.v4(),
      });
      this.updateTimeout = null;
    }, 500); // 500ms delay
  }

  ngOnDestroy(): void {

    if (this.updateTimeout) {
      clearTimeout(this.updateTimeout);
      this.storageService.Communicate({
        type: 'json-key',
        args: {
          env: 'code-editor',
          type: 'update',
          key: 'code-editor',
          value: this.code,
        },
        uuid: uuid.v4(),
      });

    }
  }
}
