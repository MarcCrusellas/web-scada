# SCADA Dashboard Roadmap

## Current Features
- Real-time data visualization using Apache ECharts.
- WebSocket communication for live updates.
- Taskbar menu for starting/stopping data transmission.

## Planned Features

### Phase 1: Dashboard and Widget System
- [ ] **Screen List Viewer**:
  - View all created screens.
  - Create new screens.
  - Edit existing screens.
- [ ] **Library Creator**:
  - Create and manage widget libraries.
  - Navigate to widget creation for a specific library.
- [ ] **Widget Creator**:
  - Allow users to create custom widgets.
  - Widgets can be added to screens.
- [ ] **Screen Editor**:
  - Drag-and-drop widgets onto screens using `angular-gridster2`.
  - Save screen layouts.

### Phase 2: Advanced Features
- [ ] **User Authentication**:
  - Role-based access control.
- [ ] **Historical Data Analysis**:
  - Add tools for analyzing trends and generating reports.
- [ ] **Alarm and Event Notifications**:
  - Show alerts for critical events.
- [ ] **Mobile-Friendly Interface**:
  - Ensure the dashboard works well on mobile devices.

### Phase 3: Deployment and Security
- [ ] **Secure WebSocket Communication**:
  - Use WSS with SSL/TLS.
- [ ] **Cloud Deployment**:
  - Deploy the SCADA system to a cloud platform.
- [ ] **Dockerization**:
  - Create Docker containers for backend and frontend.

---

Feel free to update this roadmap as new features are added or priorities change.
