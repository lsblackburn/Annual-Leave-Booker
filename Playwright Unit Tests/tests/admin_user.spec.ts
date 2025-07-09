import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => { // This function runs before each test to ensure the page is in a clean state
    await page.goto('http://127.0.0.1:5000/login');
    await page.getByRole('textbox', { name: 'Enter email' }).click();
    await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.com');
    await page.getByRole('textbox', { name: 'Enter password' }).click();
    await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
    await page.goto('http://127.0.0.1:5000/controlpanel');
});

test('Admin user updating user credentials again', async ({ page }) => { // This test checks if an admin user can update another user's credentials again
    var secondRow = page.locator('table tbody tr').nth(1);
    await secondRow.locator('#editUser').click();
    await page.getByRole('textbox', { name: 'New Password (optional)' }).click();
    await page.getByRole('textbox', { name: 'New Password (optional)' }).fill('Password123!!');
    await page.getByRole('button', { name: 'Update User' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
    await expect(page.getByText('User updated.')).toBeVisible();
});

test('Admin promoting and then demoting a user, then deleting the user', async ({ page }) => { // This test checks if an admin can promote a user to admin and then demote them back, then delete the user
    const secondRow = page.locator('table tbody tr').nth(1);

    // The following tests must be run in order to function correctly:

    // Promote
    await secondRow.getByRole('button', { name: 'Make Admin' }).click();
    await page.getByRole('button', { name: 'Yes, promote it!' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
    await expect(page.getByText('User promoted to admin.')).toBeVisible();

    // Demote
    await secondRow.getByRole('button', { name: 'Revoke Admin' }).click();
    await page.getByRole('button', { name: 'Yes, revoke it!' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
    await expect(page.getByText('User demoted from admin.')).toBeVisible();

    // Delete
    await secondRow.getByRole('button').first().click();
    await page.getByRole('button', { name: 'Yes, delete it!' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
    await expect(page.getByText('User deleted.')).toBeVisible();
});
