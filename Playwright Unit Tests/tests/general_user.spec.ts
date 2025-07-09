import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => { // This function runs before each test to ensure the page is in a clean state
    await page.goto('http://127.0.0.1:5000/login');
    await page.getByRole('textbox', { name: 'Enter email' }).click();
    await page.getByRole('textbox', { name: 'Enter email' }).fill('lewisblackburn9@gmail.com');
    await page.getByRole('textbox', { name: 'Enter password' }).click();
    await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
});

test('General user access to the admin control panel', async ({ page }) => { // This test checks if a general user can access the admin control panel
  await page.goto('http://127.0.0.1:5000/controlpanel');
  expect(page.url()).toBe('http://127.0.0.1:5000/');
  await expect(page.getByText('Access denied: Administrator privileges are required.')).toBeVisible();
});

test('General user to access user edit page', async ({ page }) => { // This test checks if a general user can access the user edit page
  await page.goto('http://127.0.0.1:5000/pending-leave');
  expect(page.url()).toBe('http://127.0.0.1:5000/');
  await expect(page.getByText('Access denied: Administrator privileges are required.')).toBeVisible();
});
