'use strict';

describe('Sandowrm App', function() {

    var baseUrl = 'http://localhost:8080/#/';

    it('should redirect to login', function() {
        browser.driver.get(baseUrl);
        expect(browser.getCurrentUrl()).toEqual(baseUrl + 'login');
    });

    it('should display login form', function() {
        browser.driver.get(baseUrl);
        expect(element(by.css('.signin-link')).isDisplayed())
            .toBe(true);
    });

    /* Role: user */
    describe('Basic lab list', function() {

        it('should login user', function() {
            browser.get(baseUrl);
            var username = element(
                by.model('ctrl.user.username'));
            var password = element(
                by.model('ctrl.user.password'));
            username.sendKeys('test');
            password.sendKeys('test');
            element(by.css('.btn.btn-primary')).click();
            expect(element(by.css('.signout-link')).isDisplayed())
                .toBe(true);
            expect(browser.getCurrentUrl()).toEqual(baseUrl + 'labs');
        });

        it('should display basic labs page', function() {
            var labList = element.all(by.repeater('lab in labCtrl.labs'));
            expect(labList.count()).toBe(2);
        });

        describe('Lab details', function() {
            
            beforeEach(function() {
                browser.driver.get(baseUrl + 'labs/lab-1');
            });

            it('should display lab details page', function() {    
                expect(element(by.binding('ctrl.lab.name')).getText()).toBe('LAB1');
            });
        });

        it('should prevent navigating to nonauthorized resource', function() {
            browser.driver.get(baseUrl + 'admin/labs/lab-1');
            expect(browser.getCurrentUrl()).toEqual(baseUrl + 'labs');
        });

        it('should sign out current user', function() {
            browser.driver.get(baseUrl);
            element(by.css('.signout-link')).click();
            expect(browser.getCurrentUrl()).toEqual(baseUrl + 'login');
            expect(element(by.css('.signin-link')).isDisplayed())
                .toBe(true);
        });

        it('should redirect to login when accessing private resource', function() {
            browser.driver.get(baseUrl + 'labs/lab-1');
            expect(browser.getCurrentUrl()).toEqual(baseUrl + 'login');
        });

    });

    /* Role: admin */
    describe('Basic admin lab list', function() {

        it('should login user', function() {
            browser.get(baseUrl);
            var username = element(
                by.model('ctrl.user.username'));
            var password = element(
                by.model('ctrl.user.password'));
            username.sendKeys('admin');
            password.sendKeys('test');
            element(by.css('.btn.btn-primary')).click();
            expect(element(by.css('.signout-link')).isDisplayed())
                .toBe(true);
            expect(browser.getCurrentUrl()).toEqual(baseUrl + 'admin/labs');
        });

        it('should display basic labs page', function() {
            var labList = element.all(by.repeater('lab in labCtrl.labs'));
            expect(labList.count()).toBe(2);
        });

        describe('Lab details', function() {
            
            beforeEach(function() {
                browser.driver.get(baseUrl + 'admin/labs/lab-1');
            });

            it('should display lab details page', function() {    
                expect(element(by.binding('ctrl.lab.name')).getText()).toBe('LAB1');
            });
        });

        describe('All results', function() {
            
            beforeEach(function() {
                browser.driver.get(baseUrl + 'admin/results');
            });

            it('should display all results page', function() {
                var labList = element.all(by.repeater('lab in ctrl.results.labs'));
                expect(labList.count()).toBe(4);
            });
        });

        it('should sign out current user', function() {
            browser.driver.get(baseUrl);
            element(by.css('.signout-link')).click();
            expect(browser.getCurrentUrl()).toEqual(baseUrl + 'login');
            expect(element(by.css('.signin-link')).isDisplayed())
                .toBe(true);
        });

        it('should redirect to login when accessing private resource', function() {
            browser.driver.get(baseUrl + 'admin/labs/lab-1');
            expect(browser.getCurrentUrl()).toEqual(baseUrl + 'login');
        });
    });
});