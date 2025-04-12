import { signal , Component} from '@angular/core';
import { StorageService } from '../core/services/storage.service';
import { CodeEditorComponent } from '../components/code-editor/code-editor.component';

@Component({
  selector: 'app-test-communication',
  templateUrl: './test-communication.component.html',
  styleUrls: ['./test-communication.component.css'],
  imports: [CodeEditorComponent],
})
export class TestCommunicationComponent {
  stateKey = signal('');
  stateValue = signal('');
  fileName = signal('');
  fileContent = signal('');

  constructor(private storageService: StorageService) {}

  testFetchState(): void {
    if (!this.stateKey().trim()) {
      alert('State key cannot be empty!');
      return;
    }
    this.storageService.fetchState(this.stateKey()).then(value => {
      this.stateValue.set(value || '');
      console.log('Fetched state:', value);
    });
  }

  testUpdateState(): void {
    if (!this.stateKey().trim()) {
      alert('State key cannot be empty!');
      return;
    }
    this.storageService.updateState(this.stateKey(), this.stateValue());
    console.log('State updated with key:', this.stateKey(), 'value:', this.stateValue());
  }

  testSetFile(): void {
    if (!this.fileName().trim()) {
      alert('File name cannot be empty!');
      return;
    }
    this.storageService.setFile(this.fileName(), this.fileContent());
    console.log('File set with name:', this.fileName());
  }

  testGetFile(): void {
    if (!this.fileName().trim()) {
      alert('File name cannot be empty!');
      return;
    }
    console.log('Fetching file with name:', this.fileName());
    this.storageService.getFile(this.fileName()).then((content: string | null) => {
      this.fileContent.set(content || '');
      console.log('Fetched file content:', content);
    });
  }

  onStateKeyChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.stateKey.set(input.value);
  }

  onStateValueChange(event: Event): void {
    const textarea = event.target as HTMLTextAreaElement;
    this.stateValue.set(textarea.value);
  }

  onFileNameChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.fileName.set(input.value);
  }

  onFileContentChange(event: Event): void {
    const textarea = event.target as HTMLTextAreaElement;
    this.fileContent.set(textarea.value);
  }
}
