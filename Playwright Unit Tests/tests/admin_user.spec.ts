import { test, expect } from '@playwright/test';

const baseURL = 'http://127.0.0.1:5000';
const credentials = {
  email: 'admin@admin.com',
  password: 'Password123!'
};

async function loginAsAdmin(page) { // Log in as admin before each test
  await page.goto(`${baseURL}/login`);
  await page.getByRole('textbox', { name: 'Enter email' }).fill(credentials.email);
  await page.getByRole('textbox', { name: 'Enter password' }).fill(credentials.password);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
  await page.goto(`${baseURL}/controlpanel`);
}

test.beforeEach(async ({ page }) => {
  await loginAsAdmin(page);
});

test('Admin updates another user\'s credentials', async ({ page }) => { // Tests for updating another user's credentials
  const secondRow = page.locator('table tbody tr').nth(1);
  await secondRow.locator('#editUser').click();

  const passwordInput = page.getByRole('textbox', { name: 'New Password (optional)' });
  await passwordInput.fill(credentials.password);

  await page.getByRole('button', { name: 'Update User' }).click();
  await page.getByRole('button', { name: 'OK' }).click();

  await expect(page.getByText('User updated.')).toBeVisible();
});

test('Admin promotes, demotes, and deletes a user', async ({ page }) => { // Tests for promoting, demoting, and deleting a user
  const secondRow = page.locator('table tbody tr').nth(1);

  // Promote to admin
  await secondRow.getByRole('button', { name: 'Make Admin' }).click();
  await page.getByRole('button', { name: 'Yes, promote it!' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
  await expect(page.getByText('User promoted to admin.')).toBeVisible();

  // Demote back to user
  await secondRow.getByRole('button', { name: 'Revoke Admin' }).click();
  await page.getByRole('button', { name: 'Yes, revoke it!' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
  await expect(page.getByText('User demoted from admin.')).toBeVisible();

  // Delete user
  await secondRow.getByRole('button').first().click(); // First buton is Delete
  await page.getByRole('button', { name: 'Yes, delete it!' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
  await expect(page.getByText('User deleted.')).toBeVisible();

  // These tests must be run in order, as the second row will change after each action
});
