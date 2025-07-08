import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => { // This function runs before each test to ensure the page is in a clean state
    await page.goto('http://127.0.0.1:5000/login');
    await page.getByRole('textbox', { name: 'Enter email' }).click();
    await page.getByRole('textbox', { name: 'Enter email' }).fill('admin@admin.com');
    await page.getByRole('textbox', { name: 'Enter password' }).click();
    await page.getByRole('textbox', { name: 'Enter password' }).fill('Password123!');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
});

test('Booking annual leave successfully', async ({ page }) => { // This test checks if the user can successfully book annual leave
  await page.getByRole('link', { name: 'Request Leave' }).click();
  await page.getByRole('textbox', { name: 'Start Date' }).fill('2025-07-16');
  await page.getByRole('textbox', { name: 'End Date' }).fill('2025-07-26');
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
  await expect(page.getByText('Leave request submitted.')).toBeVisible();
});

test('Booking annual leave end date before start date', async ({ page }) => { // This test checks if the user books annual leave with an end date before the start date then it fails
  await page.getByRole('link', { name: 'Request Leave' }).click();
  await page.getByRole('textbox', { name: 'Start Date' }).fill('2025-07-26');
  await page.getByRole('textbox', { name: 'End Date' }).fill('2025-07-16');
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
  await expect(page.getByText('End date cannot be before start date.')).toBeVisible();
});

test.describe('Approving/Rejecting Annual Leave', () => { // This block contains tests that run after a successful login
  
  test.beforeEach(async ({ page }) => { // This function runs before each test to ensure the page is in a clean state
    await page.getByRole('link', { name: 'Request Leave' }).click();
    await page.getByRole('textbox', { name: 'Start Date' }).fill('2029-11-22');
    await page.getByRole('textbox', { name: 'End Date' }).fill('2033-11-24');
    await page.getByRole('button', { name: 'Submit' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
    await page.goto('http://127.0.0.1:5000/pending-leave');
  });

  test('Approving annual leave as an Admin', async ({ page }) => { // This test checks if the Admin can approve annual leave
    await page.getByRole('row', { name: 'Admin Starting: 22/11/2029' }).getByRole('button').first().click();
    await expect(page.getByText('Leave approved.')).toBeVisible();
  });

  test('Rejecting annual leave as an Admin', async ({ page }) => { // This test checks if the Admin can reject annual leave requests
    await page.getByRole('row', { name: 'Admin Starting: 22/11/2029' }).getByRole('button').last().click();
    await expect(page.getByText('Leave rejected.')).toBeVisible();
  });


});