it('Testing picture uploading', () => {
    cy.fixture('testPicture.png').then(fileContent => {
        cy.get('input[type="file"]').attachFile({
            fileContent: fileContent.toString(),
            fileName: 'testPicture.png',
            mimeType: 'image/png'
        });
    });
});