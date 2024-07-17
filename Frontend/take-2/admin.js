document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-link');
  const pageTitle = document.querySelector('.page-title');
  const content = document.querySelector('.content');

  navLinks.forEach(link => {
      link.addEventListener('click', function(e) {
          e.preventDefault();
          const section = link.getAttribute('data-section');

          // Update active link
          navLinks.forEach(nav => nav.classList.remove('active'));
          link.classList.add('active');

          // Update page title
          pageTitle.textContent = section.charAt(0).toUpperCase() + section.slice(1);

          // Load content based on section
          loadContent(section);
      });
  });

  function loadContent(section) {
      switch (section) {
          case 'dashboard':
              content.innerHTML = '<h2>Dashboard Content</h2><p>Welcome to the admin dashboard.</p>';
              break;
          case 'users':
              content.innerHTML = `
                  <h2>Users Management</h2>
                  <form id="userForm">
                      <div class="form-group">
                          <label for="username">Username:</label>
                          <input type="text" id="username" name="username" class="form-control" required>
                      </div>
                      <div class="form-group">
                          <label for="email">Email:</label>
                          <input type="email" id="email" name="email" class="form-control" required>
                      </div>
                      <button type="submit" class="btn btn-primary">Add User</button>
                  </form>
                  <table class="table mt-3">
                      <thead>
                          <tr>
                              <th>ID</th>
                              <th>Username</th>
                              <th>Email</th>
                              <th>Actions</th>
                          </tr>
                      </thead>
                      <tbody id="userTable">
                          <!-- User data will be loaded here -->
                      </tbody>
                  </table>
              `;
              break;
          case 'settings':
              content.innerHTML = `
                  <h2>Settings</h2>
                  <form id="settingsForm">
                      <div class="form-group">
                          <label for="siteName">Site Name:</label>
                          <input type="text" id="siteName" name="siteName" class="form-control" required>
                      </div>
                      <div class="form-group">
                          <label for="adminEmail">Admin Email:</label>
                          <input type="email" id="adminEmail" name="adminEmail" class="form-control" required>
                      </div>
                      <button type="submit" class="btn btn-primary">Save Settings</button>
                  </form>
              `;
              break;
          default:
              content.innerHTML = '<h2>Dashboard Content</h2><p>Welcome to the admin dashboard.</p>';
      }
  }

  // Load default content
  loadContent('dashboard');
});
