import { test, expect } from '@playwright/test';

const baseURL = 'http://127.0.0.1:5000';

// Helper function to register and log in a new user
async function registerAndLogin(page) {
  const uniqueEmail = `testuser_${Date.now()}@example.com`;
  const password = 'Password123!';

  // Register
  await page.goto(`${baseURL}/register`);
  await page.getByRole('textbox', { name: 'Enter name' }).fill('Test User');
  await page.getByRole('textbox', { name: 'Enter email' }).fill(uniqueEmail);
  await page.getByRole('textbox', { name: 'Enter password' }).fill(password);
  await page.getByRole('textbox', { name: 'Enter confirm password' }).fill(password);
  await page.getByRole('button', { name: 'Create an account' }).click();
  await page.getByRole('button', { name: 'OK' }).click();

  // Login
  await page.goto(`${baseURL}/login`);
  await page.getByRole('textbox', { name: 'Enter email' }).fill(uniqueEmail);
  await page.getByRole('textbox', { name: 'Enter password' }).fill(password);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
}

test.beforeEach(async ({ page }) => {
  await registerAndLogin(page); // Ensure a new general user is logged in before each test
});

test('General user access to the admin control panel', async ({ page }) => { // General users should not access the admin control panel
  await page.goto(`${baseURL}/controlpanel`);
  await expect(page).toHaveURL(`${baseURL}`);
  await expect(page.getByText('Access denied: Administrator privileges are required.')).toBeVisible();
});

test('General user access to pending leave requests page', async ({ page }) => { // General users should not access the user edit page
  await page.goto(`${baseURL}/pending-leave`);
  await expect(page).toHaveURL(`${baseURL}`);
  await expect(page.getByText('Access denied: Administrator privileges are required.')).toBeVisible();
});
