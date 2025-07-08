import { test, expect } from '@playwright/test';

test('Without session, redirect to dashboard', async ({ page }) => { // This test checks if the user is redirected to the dashboard when not logged in
  await page.goto('http://127.0.0.1:5000');
  await page.getByRole('button', { name: 'OK' }).click();
  expect(page.url()).toBe('http://127.0.0.1:5000/login'); // The user should be redirected to the login page
  await expect(page.getByText('Please log in.')).toBeVisible();
});

test('Registration success', async ({ page }) => { // This test checks if the user can register successfully
  await page.goto('http://127.0.0.1:5000/register');
  await page.getByRole('textbox', { name: 'Enter name' }).click();
  await page.getByRole('textbox', { name: 'Enter name' }).fill('Test User');
  await page.getByRole('textbox', { name: 'Enter name' }).press('Tab');
  // Use a unique email for each test run to avoid "Email is already registered" error
  const uniqueEmail = `testuser_${Date.now()}@example.com`;
  await page.getByRole('textbox', { name: 'Enter email' }).fill(uniqueEmail);
  await page.getByRole('textbox', { name: 'Enter email' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
  await page.getByRole('textbox', { name: 'Enter password' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter confirm password' }).fill('Password123!');
  await page.getByRole('button', { name: 'Create an account' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
  expect(page.url()).toBe('http://127.0.0.1:5000/login'); // After a successful registration, the user should be redirected to the login page
  await expect(page.getByText('Registration successful. Please log in.')).toBeVisible();
});

test('Registration email conflicts', async ({ page }) => { // This test checks if the registration fails when trying to register as the Admin user
  await page.goto('http://127.0.0.1:5000/register');
  await page.getByRole('textbox', { name: 'Enter name' }).click();
  await page.getByRole('textbox', { name: 'Enter name' }).fill('Name');
  await page.getByRole('textbox', { name: 'Enter name' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.com');
  await page.getByRole('textbox', { name: 'Enter email' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
  await page.getByRole('textbox', { name: 'Enter password' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter confirm password' }).fill('Password123!');
  await page.getByRole('button', { name: 'Create an account' }).click();
  expect(page.url()).toBe('http://127.0.0.1:5000/register'); // After a successful registration, the user should be redirected to the login page
  await expect(page.getByText('Email is already registered.')).toBeVisible();
});

test('Registration for Admin', async ({ page }) => { // This test checks if the registration fails when trying to register as the Admin user
  await page.goto('http://127.0.0.1:5000/register');
  await page.getByRole('textbox', { name: 'Enter name' }).click();
  await page.getByRole('textbox', { name: 'Enter name' }).fill('Admin');
  await page.getByRole('textbox', { name: 'Enter name' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.com');
  await page.getByRole('textbox', { name: 'Enter email' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
  await page.getByRole('textbox', { name: 'Enter password' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter confirm password' }).fill('Password123!');
  await page.getByRole('button', { name: 'Create an account' }).click();
  expect(page.url()).toBe('http://127.0.0.1:5000/register'); // After a successful registration, the user should be redirected to the login page
  await expect(page.getByText('The name Admin is reserved and cannot be used.')).toBeVisible();
});

test('Login fail', async ({ page }) => {
  await page.goto('http://127.0.0.1:5000/login');
  await page.getByRole('textbox', { name: 'Enter email' }).click();
  await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.co.uk'); // Intentionally using a wrong email to trigger a login failure
  await page.getByRole('textbox', { name: 'Enter password' }).click();
  await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.getByRole('button', { name: 'OK' }).click(); // This triggers an error message for incorrect login
  expect(page.url()).toBe('http://127.0.0.1:5000/login'); // The user should remain on the login page after a failed login attempt
  await expect(page.getByText('Invalid email or password.')).toBeVisible(); // Check if the error message is displayed
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
    expect(page.url()).toBe('http://127.0.0.1:5000/'); // After a successful login, the user should be redirected to the dashboard
    await expect(page.getByText('Login successful!')).toBeVisible();
  });

  test('Logout success', async ({ page }) => {
    await page.getByRole('button', { name: 'OK' }).click();
    await page.getByRole('button', { name: 'Account' }).click();
    await page.getByRole('button', { name: 'Sign out' }).click(); // This logs the user out
    await page.getByRole('button', { name: 'OK' }).click(); // This confirms the logout action
    expect(page.url()).toBe('http://127.0.0.1:5000/login'); // After logging out, the user should be redirected to the login page
    await expect(page.getByText('You have been logged out.')).toBeVisible();
  });

});