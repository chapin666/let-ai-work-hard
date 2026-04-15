# Source: chapter-18-ai-automation-test.md
# Lines: 323-379
# Language: javascript

// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.selectors = {
      emailInput: '[data-testid="login-email"]',
      passwordInput: '[data-testid="login-password"]',
      submitButton: '[data-testid="login-submit"]',
      errorMessage: '[data-testid="login-error"]',
    };
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email, password) {
    await this.page.fill(this.selectors.emailInput, email);
    await this.page.fill(this.selectors.passwordInput, password);
    await this.page.click(this.selectors.submitButton);
  }

  async getErrorMessage() {
    return this.page.textContent(this.selectors.errorMessage);
  }
}

// tests/login.spec.js
describe('Login Flow', () => {
  let loginPage;
  let testUser;

  beforeEach(async () => {
    testUser = await factory.create('user', { password: 'correct-password' });
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login redirects to dashboard', async () => {
    await loginPage.login(testUser.email, 'correct-password');
    await expect(page).toHaveURL('/dashboard');
  });

  test('shows error for invalid credentials', async () => {
    await loginPage.login(testUser.email, 'wrong-password');
    const error = await loginPage.getErrorMessage();
    expect(error).toContain('邮箱或密码错误');
  });

  test('shows validation error for empty email', async () => {
    await loginPage.login('', 'some-password');
    const error = await loginPage.getErrorMessage();
    expect(error).toContain('请输入邮箱');
  });
});
