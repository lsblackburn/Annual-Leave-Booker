import { test, expect } from '@playwright/test';

test('Without session, redirect to dashboard', async ({ page }) => { // This test checks if the user is redirected to the dashboard when not logged in
  await page.goto('http://127.0.0.1:5000');
  await page.getByRole('button', { name: 'OK' }).click();
});

test('Registration success', async ({ page }) => { // This test checks if the user can register successfully
  await page.goto('http://127.0.0.1:5000/register');
  await page.getByRole('textbox', { name: 'Enter name' }).click();
  await page.getByRole('textbox', { name: 'Enter name' }).fill('Test User');
  await page.getByRole('textbox', { name: 'Enter name' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter email' }).fill('test@email.co.uk');
  await page.getByRole('textbox', { name: 'Enter email' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
  await page.getByRole('textbox', { name: 'Enter password' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter confirm password' }).fill('Password123!');
  await page.getByRole('button', { name: 'Create an account' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
});

test('Login fail', async ({ page }) => {
  await page.goto('http://127.0.0.1:5000/login');
  await page.getByRole('textbox', { name: 'Enter email' }).click();
  await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.com'); // Intentionally using a wrong email to trigger a login failure
  await page.getByRole('textbox', { name: 'Enter password' }).click();
  await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.getByRole('button', { name: 'OK' }).click(); // This triggers an error message for incorrect login
});

test.describe('Tests after login', () => { // This block contains tests that run after a successful login
  
  test.beforeEach(async ({ page }) => { // This function runs before each test to ensure the page is in a clean state
    await page.goto('http://127.0.0.1:5000/login');
    await page.getByRole('textbox', { name: 'Enter email' }).click();
    await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.com');
    await page.getByRole('textbox', { name: 'Enter password' }).click();
    await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
    await page.getByRole('button', { name: 'Sign in' }).click();
  });

  test('Login success', async ({ page }) => { // This test checks if the user can log in successfully
    await page.getByRole('button', { name: 'OK' }).click();
  });

  test('Logout success', async ({ page }) => {
    await page.getByRole('button', { name: 'OK' }).click();
    await page.getByRole('button', { name: 'Account' }).click();
    await page.getByRole('button', { name: 'Sign out' }).click(); // This logs the user out
    await page.getByRole('button', { name: 'OK' }).click(); // This confirms the logout action
  });

});