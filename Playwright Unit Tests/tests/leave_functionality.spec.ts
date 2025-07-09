import { test, expect } from '@playwright/test';

const baseURL = 'http://127.0.0.1:5000';
const credentials = {
  email: 'admin@admin.com',
  password: 'Password123!'
};

async function login(page) { // Log in the user before each test
  await page.goto(`${baseURL}/login`);
  await page.getByRole('textbox', { name: 'Enter email' }).fill(credentials.email);
  await page.getByRole('textbox', { name: 'Enter password' }).fill(credentials.password);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
}

async function requestLeave(page, startDate: string, endDate: string) { // Function to request leave
  await page.getByRole('link', { name: 'Request Leave' }).click();
  await page.getByRole('textbox', { name: 'Start Date' }).fill(startDate);
  await page.getByRole('textbox', { name: 'End Date' }).fill(endDate);
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByRole('button', { name: 'OK' }).click();
}

test.beforeEach(async ({ page }) => {
  await login(page);
});

test.describe('Annual Leave Requests', () => { // Tests for requesting annual leave functionality

  test('Booking annual leave successfully', async ({ page }) => { // Tests successful booking of annual leave
    await requestLeave(page, '2025-07-16', '2025-07-26');
    await expect(page.getByText('Leave request submitted.')).toBeVisible();
  });

  test('Booking annual leave with end date before start date', async ({ page }) => { // Tests booking annual leave with an end date before the start date cannot occur
    await requestLeave(page, '2025-07-26', '2025-07-16');
    await expect(page.getByText('End date cannot be before start date.')).toBeVisible();
  });

  test('Updating leave dates', async ({ page }) => { // Tests updating leave dates after a request has been made
    await requestLeave(page, '2029-11-22', '2033-11-24');

    // Navigate to the your leaves page
    await page.goto(`${baseURL}/your-leaves`);
    await page.getByRole('button', { name: 'Account' }).click();
    await page.getByRole('link', { name: 'Your annual leave' }).click();

    // Edit first leave entry
    await page.getByRole('button', { name: 'Edit' }).first().click();
    await page.getByRole('textbox', { name: 'Start Date' }).fill('2033-09-15');
    await page.getByRole('textbox', { name: 'End Date' }).fill('2041-11-14');
    await page.getByRole('button', { name: 'Submit' }).click();
    await page.getByRole('button', { name: 'OK' }).click();

    await expect(page.getByText('Leave updated. Awaiting admin approval.')).toBeVisible();
  });
});

test.describe('Admin Leave Approvals', () => {

  test.beforeEach(async ({ page }) => {
    await login(page);
    await requestLeave(page, '2029-11-22', '2033-11-24');
    await page.goto(`${baseURL}/pending-leave`);
  });

  test('Approving annual leave', async ({ page }) => {
    await page.getByRole('row', { name: 'Admin Starting: 22/11/2029' }).getByRole('button').first().click();
    await expect(page.getByText('Leave approved.')).toBeVisible();
  });

  test('Rejecting annual leave', async ({ page }) => {
    await page.getByRole('row', { name: 'Admin Starting: 22/11/2029' }).getByRole('button').last().click();
    await expect(page.getByText('Leave rejected.')).toBeVisible();
  });

});
