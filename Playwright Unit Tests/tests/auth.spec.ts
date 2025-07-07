import { test, expect } from '@playwright/test';

test('Without session, redirect to dashboard', async ({ page }) => {
  await page.goto('http://127.0.0.1:5000');
  await page.getByRole('button', { name: 'OK' }).click();
});

test('Login success', async ({ page }) => {
  await page.goto('http://127.0.0.1:5000');
  await page.getByRole('button', { name: 'OK' }).click();
  await page.getByRole('textbox', { name: 'Enter email' }).click();
  await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.com');
  await page.getByRole('textbox', { name: 'Enter email' }).press('Tab');
  await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
});

